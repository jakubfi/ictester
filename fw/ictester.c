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

uint8_t dut_package_type;
uint8_t dut_pin_count;

uint8_t test_type;
uint8_t test_params[MAX_TEST_PARAMS];

uint8_t cfgnum;
uint8_t cfgnum_active = NO_CONFIG;

// -----------------------------------------------------------------------
static uint8_t handle_dut_setup()
{
	uint8_t pin_data[MAX_CONFIGS][ZIF_PIN_CNT];

	// receive DUT configuration
	dut_package_type = serial_rx_char();
	dut_pin_count = serial_rx_char();
	uint8_t pincfg_cnt = serial_rx_char();
	for (uint8_t cfgnum=0 ; cfgnum<pincfg_cnt ; cfgnum++) {
		for (uint8_t i=0 ; i<dut_pin_count ; i++) {
			pin_data[cfgnum][i] = serial_rx_char();
		}
	}

	// check DUT pinout
	if (
		((dut_pin_count != 14) && (dut_pin_count != 16) && (dut_pin_count != 20) && (dut_pin_count != 24))
		|| (dut_package_type != PACKAGE_DIP)
	) {
		return RESP_ERR;
	}

	if ((pincfg_cnt < 1) || (pincfg_cnt > MAX_CONFIGS)) {
		return RESP_ERR;
	}

	zif_config_clear();

	// prepare port configuration based on provided DUT pin config
	for (uint8_t cfgnum=0 ; cfgnum<pincfg_cnt ; cfgnum++) {
		for (uint8_t i=0 ; i<dut_pin_count ; i++) {
			uint8_t zif_pin = zif_pos(dut_pin_count, i);
			if (!zif_func(cfgnum, pin_data[cfgnum][i], zif_pin)) return RESP_ERR;
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_test_setup()
{
	cfgnum = serial_rx_char();
	test_type = serial_rx_char();
	for (uint8_t i=0 ; i<MAX_TEST_PARAMS ; i++) {
		test_params[i] = serial_rx_char();
	}

	// read pin usage data
	uint8_t pin_usage[3];
	for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
		pin_usage[i/8] = serial_rx_char();
	}

	zif_pin_mask_clear(cfgnum);

	// fill in port masks
	for (uint8_t i=0 ; i<dut_pin_count ; i++) {
		uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
		if (pin_used) {
			uint8_t zif_pin = zif_pos(dut_pin_count, i);
			zif_pin_unmasked(cfgnum, zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t do_connect(uint8_t cfgnum)
{
	led(LED_ACTIVE);

	if (!zif_connect(cfgnum)) {
		return RESP_ERR;
	}

	if (test_type == TEST_DRAM) {
		mem_setup();
	}

	cfgnum_active = cfgnum;

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_connect()
{
	cfgnum = serial_rx_char();
	return do_connect(cfgnum);
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_disconnect(uint8_t resp)
{
	zif_disconnect();
	cfgnum_active = NO_CONFIG;

	if (resp == RESP_ERR) led(LED_ERR);
	else if (resp == RESP_FAIL) led(LED_FAIL);
	else if (resp == RESP_PASS) led(LED_PASS);
	else led(LED_IDLE);

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_run()
{
	uint8_t res = RESP_PASS;

	uint16_t loops = serial_rx_16le();

	if (cfgnum_active != cfgnum) {
		res = do_connect(cfgnum);
		if (res != RESP_OK) return res;
	}

	switch (test_type) {
		case TEST_LOGIC:
			res = run_logic(dut_pin_count, loops, test_params);
			break;
		case TEST_DRAM:
			res = run_mem(loops, test_params);
			break;
		case TEST_UNIVIB:
			res = run_univib(loops, test_params);
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

	while (true) {
		uint8_t resp;
		int cmd = serial_rx_char();

		switch (cmd) {
			case CMD_DUT_SETUP:
				resp = handle_dut_setup();
				break;
			case CMD_DUT_CONNECT:
				resp = handle_dut_connect();
				break;
			case CMD_TEST_SETUP:
				resp = handle_test_setup();
				break;
			case CMD_VECTORS_LOAD:
				resp = handle_vectors_load(dut_pin_count, zif_get_vcc_pin());
				break;
			case CMD_TEST_RUN:
				resp = handle_run();
				break;
			case CMD_DUT_DISCONNECT:
				resp = handle_dut_disconnect(resp);
				break;
			default:
				resp = RESP_ERR;
		}

		if (resp == RESP_ERR) {
			led(LED_ERR);
		}

		reply(resp);

		// handle response data for failed LOGIC tests
		if ((cmd == CMD_TEST_RUN) && (resp == RESP_FAIL) && (test_type == TEST_LOGIC)) {
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
