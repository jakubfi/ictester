#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/cpufunc.h>
#include <util/delay_basic.h>

#include "zif.h"
#include "mcu.h"
#include "protocol.h"
#include "serial.h"

#define MAX_VECTORS 1024

uint16_t vectors_count;
uint8_t vectors[MAX_VECTORS][MCU_PORT_CNT];
uint8_t check_result[MAX_VECTORS];

// -----------------------------------------------------------------------
uint8_t handle_vectors_load(uint8_t dut_pin_count, uint8_t zif_vcc_pin)
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
		for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
			vectors[pos][i] = 0;
			check_result[pos] = 1;
		}
		// fill in bits in MCU port pin order
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			int8_t port_pos = zif_mcu_port(zif_pin);
			uint8_t bit_val = (bitvector >> dut_pin) & 1;
			if ((zif_pin == zif_vcc_pin) && bit_val) {
				check_result[pos] = 0;
				bit_val = 0;
			}
			vectors[pos][port_pos] |= bit_val << zif_mcu_port_bit(zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic2(uint16_t delay, struct mcu_port_config *mcu_port)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTB = ((vectors[pos][PB] & mcu_port[PB].output) | mcu_port[PB].pullup);
		PORTC = ((vectors[pos][PC] & mcu_port[PC].output) | mcu_port[PC].pullup);

		if (delay) _delay_loop_2(delay);

		if (check_result[pos]) {
			if ((PINB ^ vectors[pos][PB]) & mcu_port[PB].mask) return RESP_FAIL;
			if ((PINC ^ vectors[pos][PC]) & mcu_port[PC].mask) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic3(uint16_t delay, struct mcu_port_config *mcu_port)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTA = ((vectors[pos][PA] & mcu_port[PA].output) | mcu_port[PA].pullup);
		PORTB = ((vectors[pos][PB] & mcu_port[PB].output) | mcu_port[PB].pullup);
		PORTC = ((vectors[pos][PC] & mcu_port[PC].output) | mcu_port[PC].pullup);

		if (delay) _delay_loop_2(delay);

		if (check_result[pos]) {
			if ((PINA ^ vectors[pos][PA]) & mcu_port[PA].mask) return RESP_FAIL;
			if ((PINB ^ vectors[pos][PB]) & mcu_port[PB].mask) return RESP_FAIL;
			if ((PINC ^ vectors[pos][PC]) & mcu_port[PC].mask) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint8_t run_logic(uint8_t dut_pin_count, uint16_t loops, uint8_t *params)
{
	volatile uint16_t delay = (params[1] << 8) + params[0];

	// local copy for speed (pointer known at compile time)
	struct mcu_port_config mcu_port_copy[3];
	struct mcu_port_config *mcu_port = mcu_get_port_config();
	if (!mcu_port) return RESP_ERR;
	for (uint8_t i=0 ; i<3 ; i++) mcu_port_copy[i] = mcu_port[i];

	if (dut_pin_count <= 16) {
		for (uint16_t rep=0 ; rep<loops ; rep++) {
			if (run_logic2(delay, mcu_port_copy) != RESP_PASS) return RESP_FAIL;
		}
	} else {
		for (uint16_t rep=0 ; rep<loops ; rep++) {
			if (run_logic3(delay, mcu_port_copy) != RESP_PASS) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// vim: tabstop=4 shiftwidth=4 autoindent
