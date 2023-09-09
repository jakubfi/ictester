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

uint8_t dut_package_type;
uint8_t dut_pin_count;

uint8_t test_type;
uint8_t test_params[MAX_TEST_PARAMS];

bool dut_connected;

// -----------------------------------------------------------------------
static uint8_t handle_dut_setup()
{
	uint8_t pin_data[24];

	// receive DUT configuration
	dut_package_type = serial_rx_char();
	dut_pin_count = serial_rx_char();
	for (uint8_t i=0 ; i<dut_pin_count ; i++) {
		pin_data[i] = serial_rx_char();
	}

	// check DUT pinout
	if (
		((dut_pin_count != 14) && (dut_pin_count != 16) && (dut_pin_count != 20) && (dut_pin_count != 24))
		|| (dut_package_type != PACKAGE_DIP)
	) {
		return RESP_ERR;
	}

	zif_config_clear();

	// prepare port configuration based on provided DUT pin config
	for (uint8_t i=0 ; i<dut_pin_count ; i++) {
		uint8_t zif_pin = zif_pos(dut_pin_count, i);
		if (!zif_func(pin_data[i], zif_pin)) return RESP_ERR;
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_test_setup()
{
	test_type = serial_rx_char();
	for (uint8_t i=0 ; i<MAX_TEST_PARAMS ; i++) {
		test_params[i] = serial_rx_char();
	}

	// read pin usage data
	uint8_t pin_usage[3];
	for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
		pin_usage[i/8] = serial_rx_char();
	}

	zif_clear_checked_outputs();

	// fill in port masks
	for (uint8_t i=0 ; i<dut_pin_count ; i++) {
		uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
		if (pin_used) {
			uint8_t zif_pin = zif_pos(dut_pin_count, i);
			zif_checked_output(zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_connect()
{
	led_active();

	if (!zif_connect()) {
		return RESP_ERR;
	}

	if (test_type == TEST_DRAM) {
		mem_setup();
	}

	dut_connected = true;

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_dut_disconnect(uint8_t resp)
{
	zif_disconnect();
	dut_connected = false;

	if (resp == RESP_ERR) led_err();
	else if (resp == RESP_FAIL) led_fail();
	else if (resp == RESP_PASS) led_pass();
	else led_idle();

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_run()
{
	uint8_t res = RESP_PASS;

	uint16_t loops = serial_rx_16le();

	if (!dut_connected) {
		res = handle_dut_connect();
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

	if (res != RESP_PASS) {
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
			led_err();
		}

		reply(resp);
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
