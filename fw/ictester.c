#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>

#include "serial.h"
#include "led.h"
#include "protocol.h"
#include "zif.h"

#include "logic.h"
#include "mem.h"
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
		// invalid number of DUT pins
		return RESP_ERR;
	}
	if (dut_package_type != PACKAGE_DIP) {
		// unknown package type
		return RESP_ERR;
	}
	if ((data->cfg_count < 1) || (data->cfg_count > MAX_CONFIGS)) {
		// invalid number of pin configurations
		return RESP_ERR;
	}

	zif_config_clear();

	// prepare port configuration based on provided DUT pin config
	for (uint8_t cfgnum=0 ; cfgnum<data->cfg_count ; cfgnum++) {
		zif_config_select(cfgnum);
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t pin_func = data->configs[cfgnum * dut_pin_count + dut_pin];
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			if (!zif_func(pin_func, zif_pin)) {
				// cannot set pin function, cause set downstream(?)
				return RESP_ERR;
			}
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_test_setup(struct cmd_test_setup *data)
{
	if (data->cfg_num >= MAX_CONFIGS) {
		// wrong configuration number
		// TODO: really check if configuration exists (has been set for the DUT)
		return RESP_ERR;
	}

	cfgnum = data->cfg_num;
	zif_config_select(cfgnum);
	test_type = data->test_type;

	switch (test_type) {
		case TEST_LOGIC:
			logic_test_setup(dut_pin_count, (struct logic_params*) data->params);
			break;
		case TEST_DRAM:
			mem_test_setup((struct mem_params*) data->params);
			break;
		case TEST_UNIVIB:
			univib_test_setup((struct univib_params*) data->params);
			break;
		default:
			// unknown test type
			return RESP_ERR;
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t do_connect()
{
	led(LED_ACTIVE);

	if (!zif_connect()) {
		// cannot connect the DUT, cause set downstream.
		return RESP_ERR;
	}

	if (test_type == TEST_DRAM) {
		mem_init();
	}

	cfgnum_active = cfgnum;

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
			res = run_logic(dut_pin_count, data->loops);
			break;
		case TEST_DRAM:
			res = run_mem(data->loops);
			break;
		case TEST_UNIVIB:
			res = run_univib(data->loops);
			break;
		default:
			// unknown test type
			res = RESP_ERR;
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
	struct cmd *cmd;

	while (true) {
		if (!receive_cmd(buf, BUF_SIZE)) {
			// command didn't fit in the buffer
			resp = RESP_ERR;
		} else {
			cmd = (struct cmd*) buf;
			switch (cmd->cmd) {
				case CMD_DUT_SETUP:
					resp = handle_dut_setup((struct cmd_dut_setup*) cmd->data);
					break;
				case CMD_DUT_CONNECT:
					resp = handle_dut_connect((struct cmd_dut_connect*) cmd->data);
					break;
				case CMD_TEST_SETUP:
					resp = handle_test_setup((struct cmd_test_setup*) cmd->data);
					break;
				case CMD_VECTORS_LOAD:
					resp = handle_vectors_load((struct vectors*) cmd->data, dut_pin_count, zif_get_vcc_pin());
					break;
				case CMD_TEST_RUN:
					resp = handle_run((struct cmd_run*) cmd->data);
					break;
				case CMD_DUT_DISCONNECT:
					resp = handle_dut_disconnect(resp);
					break;
				default:
					// unknown command
					resp = RESP_ERR;
			}
		}

		if (resp == RESP_ERR) {
			led(LED_ERR);
		}

		reply(resp);

		// handle response data for failed LOGIC tests
		if ((resp == RESP_FAIL) && (test_type == TEST_LOGIC) && (cmd->cmd == CMD_TEST_RUN)) {
			uint8_t pin_data[3] = {0, 0, 0};
			uint8_t *failed_vector = get_failed_vector();
			// translate vector from MCU port order to natural DUT pin order
			for (uint8_t pin=0 ; pin<dut_pin_count ; pin++) {
				uint8_t zif_pin = zif_pos(dut_pin_count, pin);
				uint8_t mcu_port = zif_mcu_port(zif_pin);
				uint8_t mcu_port_bit = zif_mcu_port_bit(zif_pin);
				bool bit = failed_vector[mcu_port] & _BV(mcu_port_bit);
				pin_data[pin / 8] |= bit << (pin % 8);
			}
			serial_tx_16le(get_failed_vector_pos());
			serial_tx_bytes(pin_data, 2);
			if (dut_pin_count > 16) serial_tx_char(pin_data[2]);
		}

	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
