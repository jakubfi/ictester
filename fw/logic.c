#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/cpufunc.h>

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
void handle_vectors_load(uint8_t pin_count)
{
	vectors_count = serial_rx_16le();

	// receive all vectors
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t i=0 ; i<pin_count ; i+=8) {
			vectors[pos][i/8] = serial_rx_char();
		}
	}

	// reorder bits in each vector to match port connections
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<pin_count ; i+=8) {
			bitvector |= (uint32_t)vectors[pos][i/8] << (i);
		}
		// clear received vector data
		for (uint8_t i=0 ; i<3 ; i++) {
			vectors[pos][i] = 0;
		}
		// fill in bits in correct positions
		for (uint8_t pin=0 ; pin<pin_count ; pin++) {
			uint8_t zif_pin = zif_pos(pin_count, pin);
			int8_t port_pos = mcu_port(zif_pin);
			if (port_pos >= 0) {
				uint8_t bit_val = (bitvector >> pin) & 1;
				vectors[pos][port_pos] |= bit_val << mcu_port_pin(zif_pin);
			}
		}
	}
	reply(RESP_OK);
}

// -----------------------------------------------------------------------
uint8_t run_logic(void)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// set outputs
		PORTA = ((vectors[pos][0] & port[0].dut_input) | port[0].dut_pullup);
		PORTB = ((vectors[pos][1] & port[1].dut_input) | port[1].dut_pullup);
		PORTC = ((vectors[pos][2] & port[2].dut_input) | port[2].dut_pullup);

		// read outputs
		if ((test_type == TYPE_COMB) || (pos % 2)) {
			if ((PINA ^ vectors[pos][0]) & port[0].used_outputs) return RESP_FAIL;
			if ((PINB ^ vectors[pos][1]) & port[1].used_outputs) return RESP_FAIL;
			if ((PINC ^ vectors[pos][2]) & port[2].used_outputs) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// vim: tabstop=4 shiftwidth=4 autoindent
