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

extern uint8_t dut_pin_count;
uint16_t vectors_count;
uint8_t vectors[MAX_VECTORS][3];
uint8_t check_output[MAX_VECTORS];

extern uint8_t test_type;
extern uint8_t zif_vcc_pin;

extern struct mcu_port_config {
	uint8_t output;
	uint8_t input;
	uint8_t pullup;
	uint8_t output_mask;
} mcu_port[3];

// -----------------------------------------------------------------------
uint8_t handle_vectors_load(uint8_t dut_pin_count)
{
	vectors_count = serial_rx_16le();

	// receive all vectors (bits in DUT pin order))
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
			vectors[pos][i/8] = serial_rx_char();
		}
	}

	// reorder bits in each vector into MCU port pin order
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
			bitvector |= (uint32_t) vectors[pos][i/8] << i;
		}
		// clear received vector data
		for (uint8_t i=0 ; i<3 ; i++) {
			vectors[pos][i] = 0;
			check_output[pos] = 1;
		}
		// fill in bits in MCU port pin order
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			int8_t port_pos = get_mcu_port(zif_pin);
			uint8_t bit_val = (bitvector >> dut_pin) & 1;
			if ((zif_pin == zif_vcc_pin) && bit_val) {
				check_output[pos] = 0;
				bit_val = 0;
			}
			vectors[pos][port_pos] |= bit_val << get_mcu_port_bit(zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic2(uint16_t delay)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTB = ((vectors[pos][1] & mcu_port[1].output) | mcu_port[1].pullup);
		PORTC = ((vectors[pos][2] & mcu_port[2].output) | mcu_port[2].pullup);

		if (delay) _delay_loop_2(delay);

		if (check_output[pos]) {
			if ((PINB ^ vectors[pos][1]) & mcu_port[1].output_mask) return RESP_FAIL;
			if ((PINC ^ vectors[pos][2]) & mcu_port[2].output_mask) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic3(uint16_t delay)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTA = ((vectors[pos][0] & mcu_port[0].output) | mcu_port[0].pullup);
		PORTB = ((vectors[pos][1] & mcu_port[1].output) | mcu_port[1].pullup);
		PORTC = ((vectors[pos][2] & mcu_port[2].output) | mcu_port[2].pullup);

		if (delay) _delay_loop_2(delay);

		if (check_output[pos]) {
			if ((PINA ^ vectors[pos][0]) & mcu_port[0].output_mask) return RESP_FAIL;
			if ((PINB ^ vectors[pos][1]) & mcu_port[1].output_mask) return RESP_FAIL;
			if ((PINC ^ vectors[pos][2]) & mcu_port[2].output_mask) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint8_t run_logic(uint16_t loops, uint8_t *params)
{
	volatile uint16_t delay = (params[1] << 8) + params[0];

	if (dut_pin_count <= 16) {
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
