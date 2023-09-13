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

static uint16_t vectors_count;
static struct vector {
	uint8_t check;
	struct port {
		uint8_t in, out;
	} port[MCU_PORT_CNT];
} vectors[MAX_VECTORS];

// -----------------------------------------------------------------------
uint8_t handle_vectors_load(uint8_t dut_pin_count, uint8_t zif_vcc_pin)
{
	vectors_count = serial_rx_16le();

	// receive all vectors (bits in DUT pin order))
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
			vectors[pos].port[i/8].out= serial_rx_char();
		}
	}

	// reorder bits in each vector into MCU port pin order
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<dut_pin_count ; i+=8) {
			bitvector |= (uint32_t) vectors[pos].port[i/8].out << i;
		}
		// clear received vector data
		for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
			vectors[pos].port[i].out = 0;
			vectors[pos].check = 1;
		}
		// fill in bits in MCU port pin order
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			int8_t port_pos = zif_mcu_port(zif_pin);
			uint8_t bit_val = (bitvector >> dut_pin) & 1;
			if ((zif_pin == zif_vcc_pin) && bit_val) {
				vectors[pos].check = 0;
				bit_val = 0;
			}
			vectors[pos].port[port_pos].out |= bit_val << zif_mcu_port_bit(zif_pin);
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic2(uint16_t delay, struct mcu_port_config *mcu_port)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTB = vectors[pos].port[PB].in;
		PORTC = vectors[pos].port[PC].in;

		if (!vectors[pos].check) continue;
		if (delay) _delay_loop_2(delay);

		if ((PINB & mcu_port[PB].mask) != vectors[pos].port[PB].out) return RESP_FAIL;
		if ((PINC & mcu_port[PC].mask) != vectors[pos].port[PC].out) return RESP_FAIL;
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t run_logic3(uint16_t delay, struct mcu_port_config *mcu_port)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		PORTA = vectors[pos].port[PA].in;
		PORTB = vectors[pos].port[PB].in;
		PORTC = vectors[pos].port[PC].in;

		if (!vectors[pos].check) continue;
		if (delay) _delay_loop_2(delay);

		if ((PINA & mcu_port[PA].mask) != vectors[pos].port[PA].out) return RESP_FAIL;
		if ((PINB & mcu_port[PB].mask) != vectors[pos].port[PB].out) return RESP_FAIL;
		if ((PINC & mcu_port[PC].mask) != vectors[pos].port[PC].out) return RESP_FAIL;
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint8_t run_logic(uint8_t dut_pin_count, uint16_t loops, uint8_t *params)
{
	volatile uint16_t delay = (params[1] << 8) + params[0];

	// local copy for speed (pointer known at compile time)
	struct mcu_port_config mcu_port_copy[MCU_PORT_CNT];
	struct mcu_port_config *mcu_port = mcu_get_port_config();
	if (!mcu_port) return RESP_ERR;
	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) mcu_port_copy[i] = mcu_port[i];

	// precompute input/output vectors with port masks
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t port=0 ; port<MCU_PORT_CNT ; port++) {
			vectors[pos].port[port].in = (vectors[pos].port[port].out & mcu_port[port].output) | mcu_port[port].pullup;
			vectors[pos].port[port].out &= mcu_port[port].mask;
		}
	}

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
