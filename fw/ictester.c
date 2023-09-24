#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>

#include "serial.h"
#include "led.h"
#include "protocol.h"
#include "zif.h"

#include "logic.h"
#include "dram.h"
#include "univib.h"

#define LINK_SPEED 500000
#define NO_CONFIG -1
#define BUF_SIZE 2048
uint8_t buf[BUF_SIZE];

uint8_t dut_package_type;
uint8_t dut_pin_count;
uint8_t test_type;

uint8_t cfgnum;
uint8_t cfgnum_active = NO_CONFIG;

// -----------------------------------------------------------------------
static uint8_t handle_dut_setup(struct cmd_dut_setup *data)
{
	dut_package_type = data->package;
	dut_pin_count = data->pin_count;

	if ((dut_pin_count != 14) && (dut_pin_count != 16) && (dut_pin_count != 20) && (dut_pin_count != 24)) {
		return error(ERR_PIN_CNT);
	}
	if (dut_package_type != PACKAGE_DIP) {
		return error(ERR_PACKAGE);
	}
	if ((data->cfg_count < 1) || (data->cfg_count > MAX_CONFIGS)) {
		return error(ERR_PINCFG_CNT);
	}

	zif_config_clear();

	// prepare port configuration based on provided DUT pin config
	for (uint8_t cfgnum=0 ; cfgnum<data->cfg_count ; cfgnum++) {
		zif_config_select(cfgnum);
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t pin_func = data->configs[cfgnum * dut_pin_count + dut_pin];
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			if (!zif_func(pin_func, zif_pin)) {
				return RESP_ERR; // cause set downstream
			}
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_test_setup(struct cmd_test_setup *data)
{
	if (data->cfg_num >= MAX_CONFIGS) {
		// TODO: really check if configuration exists (has been set for the DUT)
		return error(ERR_PINCFG_NUM);
	}

	cfgnum = data->cfg_num;
	zif_config_select(cfgnum);
	test_type = data->test_type;

	uint8_t resp = RESP_OK;

	switch (test_type) {
		case TEST_LOGIC:
			resp = logic_test_setup(dut_pin_count, (struct logic_params*) data->params);
			break;
		case TEST_DRAM:
			resp = dram_test_setup((struct dram_params*) data->params);
			break;
		case TEST_UNIVIB:
			resp = univib_test_setup((struct univib_params*) data->params);
			break;
		default:
			resp = error(ERR_TEST_TYPE);
	}

	return resp;
}

// -----------------------------------------------------------------------
static uint8_t do_connect()
{
	led(LED_ACTIVE);

	if (!zif_connect()) {
		return RESP_ERR; // cause set downstream.
	}

	cfgnum_active = cfgnum;

	// device specific "connects"
	if (test_type == TEST_DRAM) {
		dram_connect();
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_connect(struct cmd_dut_connect *data)
{
	cfgnum = data->cfg_num;
	zif_config_select(cfgnum);
	return do_connect();
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_disconnect(uint8_t resp)
{
	zif_disconnect();
	cfgnum_active = NO_CONFIG;

	switch (resp) {
		case RESP_ERR: led(LED_ERR); break;
		case RESP_FAIL: led(LED_FAIL); break;
		case RESP_PASS: led(LED_PASS); break;
		default: led(LED_IDLE); break;
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_run(struct cmd_run *data)
{
	uint8_t res = RESP_PASS;

	if (cfgnum_active != cfgnum) {
		res = do_connect();
		if (res != RESP_OK) return res;
	}

	switch (test_type) {
		case TEST_LOGIC:
			res = logic_run(dut_pin_count, data->loops);
			break;
		case TEST_DRAM:
			res = dram_run(data->loops);
			break;
		case TEST_UNIVIB:
			res = univib_run(data->loops);
			break;
		default:
			res = error(ERR_TEST_TYPE);
			break;
	}

	if (res == RESP_FAIL) {
		handle_dut_disconnect(res);
	}

	return res;
}

// -----------------------------------------------------------------------
int main()
{
	zif_init();
	serial_init(LINK_SPEED);
	led_init();
	led_welcome();

	uint8_t resp;
	uint8_t cmd;
	uint8_t *data = buf+1;

	while (true) {
		if (!receive_cmd(buf, BUF_SIZE)) {
			resp = error(ERR_CMD_TOOBIG);
		} else {
			cmd = buf[0];
			switch (cmd) {
				case CMD_DUT_SETUP:
					resp = handle_dut_setup((struct cmd_dut_setup*) data);
					break;
				case CMD_DUT_CONNECT:
					resp = handle_dut_connect((struct cmd_dut_connect*) data);
					break;
				case CMD_TEST_SETUP:
					resp = handle_test_setup((struct cmd_test_setup*) data);
					break;
				case CMD_VECTORS_LOAD:
					resp = logic_vectors_load((struct vectors*) data, dut_pin_count, zif_get_vcc_pin());
					break;
				case CMD_TEST_RUN:
					resp = handle_run((struct cmd_run*) data);
					break;
				case CMD_DUT_DISCONNECT:
					resp = handle_dut_disconnect(resp);
					break;
				default:
					resp = error(ERR_CMD_UNKNOWN);
			}
		}

		buf[0] = resp;
		uint16_t count = 1;

		if (resp == RESP_ERR) {
			led(LED_ERR);
			count += 1;
			buf[1] = get_error();
		} else if (resp == RESP_FAIL) {
			switch (test_type) {
				case TEST_LOGIC:
					count += logic_store_result(buf+1, dut_pin_count);
					break;
				case TEST_DRAM:
					count += dram_store_result(buf+1, dut_pin_count);
					break;
				default:
					// test does not store result data
					break;
			}
		}

		send_response(buf, count);
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
