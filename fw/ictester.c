#define F_CPU	16000000UL

#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "protocol.h"
#include "serial.h"
#include "portmap.h"
#include "mem.h"

#define MAX_VECTORS 1024

// --- DUT SETUP
struct port {
	uint8_t dut_input;
	uint8_t dut_output;
	uint8_t dut_pullup;
	uint8_t test_pin_mask;
} port[3];
uint8_t package_type;
uint8_t pin_count;
uint8_t dut_pin_bytes;

// --- TEST SETUP
uint8_t test_type;
uint8_t test_params[MAX_TEST_PARAMS];

// --- VECTORS
uint16_t vectors_count;
uint8_t vectors[MAX_VECTORS][3];

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
	dut_pin_bytes = (pin_count+7) / 8; // round up to full byte
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
	for (uint8_t i=0 ; i< MAX_TEST_PARAMS ; i++) {
		test_params[i] = serial_rx_char();
	}

	// reset port masks
	port[0].test_pin_mask = 0;
	port[1].test_pin_mask = 0;
	port[2].test_pin_mask = 0;

	// read pin usage data
	uint8_t pin_usage[3];
	for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
		pin_usage[i] = serial_rx_char();
	}

	// fill in port masks
	for (uint8_t i=0 ; i<pin_count ; i++) {
		int8_t port_pos = mcu_port(i);
		if (port_pos >= 0) {
			uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
			uint8_t port_val = pin_used << mcu_port_pin(i);
			port[port_pos].test_pin_mask |= port[port_pos].dut_output & port_val;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
void handle_vectors_load(void)
{
	vectors_count = serial_rx_16le();

	// receive all vectors
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
			vectors[pos][i] = serial_rx_char();
		}
	}

	// reorder bits in each vector to match port connections
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
			bitvector |= (uint32_t)vectors[pos][i] << (i*8);
		}
		// clear received vector data
		for (uint8_t i=0 ; i<3 ; i++) {
			vectors[pos][i] = 0;
		}
		// fill in bits in correct positions
		for (uint8_t pin=0 ; pin<pin_count ; pin++) {
			int8_t port_pos = mcu_port(pin);
			if (port_pos >= 0) {
				uint8_t bit_val = (bitvector >> pin) & 1;
				vectors[pos][port_pos] |= bit_val << mcu_port_pin(pin);
			}
		}
	}
	reply(RESP_OK);
}

// -----------------------------------------------------------------------
static inline void logic_port_setup(uint16_t pos)
{
	PORTA = ((vectors[pos][0] & port[0].dut_input) | port[0].dut_pullup);
	PORTB = ((vectors[pos][1] & port[1].dut_input) | port[1].dut_pullup);
	PORTC = ((vectors[pos][2] & port[2].dut_input) | port[2].dut_pullup);
}

// -----------------------------------------------------------------------
static inline bool logic_port_check(uint16_t pos)
{
	if ((test_type == TYPE_COMB) || (pos % 2)) {
		if ((PINA ^ vectors[pos][0]) & port[0].test_pin_mask) return false;
		if ((PINB ^ vectors[pos][1]) & port[1].test_pin_mask) return false;
		if ((PINC ^ vectors[pos][2]) & port[2].test_pin_mask) return false;
	}

	return true;
}

// -----------------------------------------------------------------------
uint8_t run_logic(void)
{
	// Seems that due to weak pull-ups in atmega, OC outputs take much longer to set up
	// Treat them separately to not slow down the test loop
	// ICs sensitive to that are: 7447, 74H62, 7489, 74156, 74170, 780101
	if (port[0].dut_pullup | port[1].dut_pullup | port[2].dut_pullup) {
		for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
			logic_port_setup(pos);
			_NOP(); _NOP(); _NOP(); _NOP(); _NOP();
			_NOP(); _NOP(); _NOP(); _NOP(); _NOP();
			if (!logic_port_check(pos)) return RESP_FAIL;
		}
	} else {
		// ~3.9us per test cycle
		for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
			logic_port_setup(pos);
			if (!logic_port_check(pos)) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
void run(void)
{
	uint8_t res = RESP_PASS;

	uint16_t test_loops = serial_rx_16le();

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
	serial_init(500000);

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
				handle_vectors_load();
				break;
			case CMD_TEST_RUN:
				run();
				break;
			default:
				reply(RESP_ERR);
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
