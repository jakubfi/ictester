#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "protocol.h"
#include "serial.h"
#include "portmap.h"
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
void deconfigure(void)
{
	DDRA = 0;
	PORTA = 0;
	DDRB = 0;
	PORTB = 0;
	DDRC = 0;
	PORTC = 0;
}

// -----------------------------------------------------------------------
void setup(void)
{
	// DUT input == MCU output
	DDRA = port[0].dut_input;
	DDRB = port[1].dut_input;
	DDRC = port[2].dut_input;
}

// -----------------------------------------------------------------------
void handle_dut_setup(void)
{
	uint8_t pin_data[24];

	// receive DUT configuration
	package_type = serial_rx_char();
	pin_count = serial_rx_char();
	for (uint8_t i=0 ; i<pin_count ; i++) {
		pin_data[i] = serial_rx_char();
	}

	// guess which socket IC uses
	if (!guess_socket(pin_count, pin_data)) {
		reply(RESP_ERR);
		return;
	}

	// clear current DUT configuration
	for (uint8_t i=0 ; i<3 ; i++) {
		port[i].dut_output = 0;
		port[i].dut_input = 0;
		port[i].dut_pullup = 0;
	}

	// prepare port configuration based on provided DUT pin config
	for (uint8_t i=0 ; i<pin_count ; i++) {
		// nothing to do for non-I/O pins
		if (pin_data[i] > PIN_OC) continue;

		int8_t port_pos = mcu_port(i);
		if (port_pos < 0) {
			// I/O pin is not connected to MCU. Shouldn't happen -> error
			reply(RESP_ERR);
			return;
		}
		uint8_t port_val = 1 << mcu_port_pin(i);
		switch (pin_data[i]) {
			case PIN_IN:
				port[port_pos].dut_input |= port_val;
				break;
			case PIN_OUT:
				port[port_pos].dut_output |= port_val;
				break;
			case PIN_OC:
				port[port_pos].dut_output |= port_val;
				port[port_pos].dut_pullup |= port_val;
				break;
			default:
				break;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
void handle_test_setup(void)
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
		int8_t port_pos = mcu_port(i);
		if (port_pos >= 0) {
			uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
			uint8_t pin_mask = pin_used << mcu_port_pin(i);
			port[port_pos].used_outputs |= port[port_pos].dut_output & pin_mask;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
void handle_run(void)
{
	uint8_t res = RESP_PASS;

	uint16_t test_loops = serial_rx_16le();

	// TODO: should be generalized in the end
	if (test_type == TYPE_MEM) {
		mem_setup();
	} else {
		setup();
	}

	for (int rep=0 ; rep<test_loops ; rep++) {
		if (test_type == TYPE_MEM) {
			res = run_mem(test_params);
		} else {
			res = run_logic();
		}
		if (res != RESP_PASS) break;
	}

	deconfigure();

	reply(res);
}

// -----------------------------------------------------------------------
int main(void)
{
	deconfigure();
	serial_init(LINK_SPEED);

	while (1) {
		int cmd = serial_rx_char();
		switch (cmd) {
			case CMD_DUT_SETUP:
				handle_dut_setup();
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
			default:
				reply(RESP_ERR);
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
