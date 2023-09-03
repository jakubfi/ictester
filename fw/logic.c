#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/cpufunc.h>
#include <util/delay_basic.h>

#include "zif.h"
#include "protocol.h"
#include "serial.h"

#define MAX_VECTORS 1024

extern uint8_t pin_count;
uint16_t vectors_count;
uint8_t vectors[MAX_VECTORS][3];

extern uint8_t test_type;

extern struct port {
	uint8_t dut_input;
	uint8_t dut_output;
	uint8_t dut_pullup;
	uint8_t used_outputs;
} port[3];

// -----------------------------------------------------------------------
uint8_t handle_vectors_load(uint8_t pin_count)
{
	vectors_count = serial_rx_16le();

	// receive all vectors (bits in DUT pin order))
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t i=0 ; i<pin_count ; i+=8) {
			vectors[pos][i/8] = serial_rx_char();
		}
	}

	// reorder bits in each vector into MCU port pin order
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<pin_count ; i+=8) {
			bitvector |= (uint32_t) vectors[pos][i/8] << i;
		}
		// clear received vector data
		for (uint8_t i=0 ; i<3 ; i++) {
			vectors[pos][i] = 0;
		}
		// fill in bits in MCU port pin order
		for (uint8_t dut_pin=0 ; dut_pin<pin_count ; dut_pin++) {
			uint8_t zif_pin = zif_pos(pin_count, dut_pin);
			int8_t port_pos = mcu_port(zif_pin);
			uint8_t bit_val = (bitvector >> dut_pin) & 1;
			vectors[pos][port_pos] |= bit_val << mcu_port_pin(zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic2(uint16_t delay)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTB = ((vectors[pos][1] & port[1].dut_input) | port[1].dut_pullup);
		PORTC = ((vectors[pos][2] & port[2].dut_input) | port[2].dut_pullup);

		if (delay) _delay_loop_2(delay);

		if ((test_type == TYPE_COMB) || (pos % 2)) {
			if ((PINB ^ vectors[pos][1]) & port[1].used_outputs) return RESP_FAIL;
			if ((PINC ^ vectors[pos][2]) & port[2].used_outputs) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic3(uint16_t delay)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTA = ((vectors[pos][0] & port[0].dut_input) | port[0].dut_pullup);
		PORTB = ((vectors[pos][1] & port[1].dut_input) | port[1].dut_pullup);
		PORTC = ((vectors[pos][2] & port[2].dut_input) | port[2].dut_pullup);

		if (delay) _delay_loop_2(delay);

		if ((test_type == TYPE_COMB) || (pos % 2)) {
			if ((PINA ^ vectors[pos][0]) & port[0].used_outputs) return RESP_FAIL;
			if ((PINB ^ vectors[pos][1]) & port[1].used_outputs) return RESP_FAIL;
			if ((PINC ^ vectors[pos][2]) & port[2].used_outputs) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint8_t run_logic(uint16_t loops, uint8_t *params)
{
	volatile uint16_t delay = (params[1] << 8) + params[0];

	if (pin_count <= 16) {
		for (uint16_t rep=0 ; rep<loops ; rep++) {
			if (run_logic2(delay) != RESP_PASS) return RESP_FAIL;
		}
	} else {
		for (uint16_t rep=0 ; rep<loops ; rep++) {
			if (run_logic3(delay) != RESP_PASS) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// vim: tabstop=4 shiftwidth=4 autoindent
