#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "serial.h"
#include "led.h"
#include "protocol.h"
#include "zif.h"
#include "logic.h"
#include "mem.h"

#define LINK_SPEED 500000

struct port {
	uint8_t dut_input;
	uint8_t dut_output;
	uint8_t dut_pullup;
	uint8_t used_outputs;
} port[3];
uint8_t package_type;
uint8_t pin_count;

uint8_t test_type;
uint8_t test_params[MAX_TEST_PARAMS];

// -----------------------------------------------------------------------
static void mcu_port_deconfigure(void)
{
	DDRA = 0;
	PORTA = 0;
	DDRB = 0;
	PORTB = 0;
	DDRC = 0;
	PORTC = 0;
}

// -----------------------------------------------------------------------
static void mcu_port_setup(void)
{
	// DUT input == MCU output
	DDRA = port[0].dut_input;
	DDRB = port[1].dut_input;
	DDRC = port[2].dut_input;
	// pullups
	PORTA = port[0].dut_pullup;
	PORTB = port[1].dut_pullup;
	PORTC = port[2].dut_pullup;
}

// -----------------------------------------------------------------------
static void handle_dut_setup(void)
{
	uint8_t res = RESP_OK;
	uint8_t pin_data[24];

	// receive DUT configuration
	package_type = serial_rx_char();
	pin_count = serial_rx_char();
	for (uint8_t i=0 ; i<pin_count ; i++) {
		pin_data[i] = serial_rx_char();
	}

	// check DUT pinout
	if (((pin_count != 14) && (pin_count != 16) && (pin_count != 20) && (pin_count != 24)) || (package_type != PACKAGE_DIP)) {
		res = RESP_ERR;
		goto fin;
	}

	// clear current DUT configuration
	for (uint8_t i=0 ; i<3 ; i++) {
		port[i].dut_output = 0;
		port[i].dut_input = 0;
		port[i].dut_pullup = 0;
	}

	// prepare port configuration based on provided DUT pin config
	for (uint8_t i=0 ; i<pin_count ; i++) {
		uint8_t zif_pin = zif_pos(pin_count, i);
		int8_t port_pos = mcu_port(zif_pin);
		uint8_t port_val = 1 << mcu_port_pin(zif_pin);
		switch (pin_data[i]) {
			case ZIF_OUT:
				port[port_pos].dut_input |= port_val;
				break;
			case ZIF_IN:
				port[port_pos].dut_output |= port_val;
				break;
			case ZIF_IN_PU_WEAK:
				port[port_pos].dut_output |= port_val;
				port[port_pos].dut_pullup |= port_val;
				break;
			case ZIF_IN_PU_STRONG:
				port[port_pos].dut_output |= port_val;
				zif_func(ZIF_IN_PU_STRONG, zif_pin);
				break;
			case ZIF_VCC:
				if (!zif_func(ZIF_VCC, zif_pin)) {
					res = RESP_ERR;
					goto fin;
				}
				break;
			case ZIF_GND:
				if (!zif_func(ZIF_GND, zif_pin)) {
					res = RESP_ERR;
					goto fin;
				}
				break;
			default:
				break;
		}
	}
fin:
	reply(res);
}

// -----------------------------------------------------------------------
static void handle_test_setup(void)
{
	test_type = serial_rx_char();
	for (uint8_t i=0 ; i<MAX_TEST_PARAMS ; i++) {
		test_params[i] = serial_rx_char();
	}

	// reset port masks
	port[0].used_outputs = 0;
	port[1].used_outputs = 0;
	port[2].used_outputs = 0;

	// read pin usage data
	uint8_t pin_usage[3];
	for (uint8_t i=0 ; i<pin_count ; i+=8) {
		pin_usage[i/8] = serial_rx_char();
	}

	// fill in port masks
	for (uint8_t i=0 ; i<pin_count ; i++) {
		uint8_t zif_pin = zif_pos(pin_count, i);
		int8_t port_pos = mcu_port(zif_pin);
		if (port_pos >= 0) {
			uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
			uint8_t pin_mask = pin_used << mcu_port_pin(zif_pin);
			port[port_pos].used_outputs |= port[port_pos].dut_output & pin_mask;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
static void handle_run(void)
{
	uint8_t res = RESP_PASS;

	uint16_t test_loops = serial_rx_16le();

	if (test_type == TYPE_MEM) {
		for (uint16_t rep=0 ; rep<test_loops ; rep++) {
			if ((res = run_mem(test_params)) != RESP_PASS) goto fin;
		}
	} else if (pin_count <= 16) {
		for (uint16_t rep=0 ; rep<test_loops ; rep++) {
			if ((res = run_logic2()) != RESP_PASS) goto fin;
		}
	} else {
		for (uint16_t rep=0 ; rep<test_loops ; rep++) {
			if ((res = run_logic3()) != RESP_PASS) goto fin;
		}
	}

fin:

	if (res == RESP_PASS) led_ok();
	else led_fail();

	reply(res);
}

// -----------------------------------------------------------------------
static void handle_dut_connect(void)
{
	led_active();
	mcu_port_setup();
	if (!zif_connect()) {
		reply(RESP_ERR);
	}

	if (test_type == TYPE_MEM) {
		mem_setup();
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
static void handle_dut_disconnect(void)
{
	zif_disconnect();
	mcu_port_deconfigure();
	reply(RESP_OK);
}

// -----------------------------------------------------------------------
int main(void)
{
	mcu_port_deconfigure();
	serial_init(LINK_SPEED);
	zif_init();
	led_init();
	led_welcome();

	while (1) {
		int cmd = serial_rx_char();
		switch (cmd) {
			case CMD_DUT_SETUP:
				handle_dut_setup();
				led_comm();
				break;
			case CMD_DUT_CONNECT:
				handle_dut_connect();
				break;
			case CMD_TEST_SETUP:
				handle_test_setup();
				break;
			case CMD_VECTORS_LOAD:
				handle_vectors_load(pin_count);
				break;
			case CMD_TEST_RUN:
				handle_run();
				break;
			case CMD_DUT_DISCONNECT:
				handle_dut_disconnect();
				break;
			default:
				reply(RESP_ERR);
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
