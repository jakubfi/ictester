#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/cpufunc.h>
#include <util/delay_basic.h>
#include <util/delay.h>

#include "zif.h"
#include "mcu.h"
#include "protocol.h"
#include "serial.h"
#include "isense.h"

#define MAX_VECTORS 1024

static uint16_t vectors_count;
static struct vector {
	uint8_t check;
	struct port {
		uint8_t in, out;
	} port[MCU_PORT_CNT];
} vectors[MAX_VECTORS];

static uint16_t delay;
static uint16_t rep;
static uint8_t failed_vector[MCU_PORT_CNT];
static uint16_t failed_vector_pos;

// -----------------------------------------------------------------------
uint8_t logic_test_setup(uint8_t dut_pin_count, struct logic_params *params)
{
	delay = params->delay;
	vectors_count = 0;

	struct mcu_port_config *mcu_port = mcu_get_port_config();
	if (!mcu_port) {
		return error(ERR_NO_PINCFG);
	}

	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
		mcu_port[i].mask = 0;
	}

	// fill in port masks
	for (uint8_t i=0 ; i<dut_pin_count ; i++) {
		uint8_t pin_used = (params->pin_usage[i/8] >> (i%8)) & 1;
		if (pin_used) {
			uint8_t zif_pin = zif_pos(dut_pin_count, i);
			int8_t port_pos = zif_mcu_port(zif_pin);
			mcu_port[port_pos].mask |= _BV(zif_mcu_port_bit(zif_pin));
		}
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
uint8_t logic_vectors_load(struct vectors *data, uint8_t dut_pin_count, uint8_t zif_vcc_pin)
{
	uint16_t chunk_vectors_count = data->vector_cnt;
	uint8_t *vector_slice = data->vectors;
	struct vector *v = vectors + vectors_count;
	vectors_count += chunk_vectors_count;

	if (vectors_count > MAX_VECTORS) {
		return error(ERR_VECT_NUM);
	}

	// reorder bits in each vector into MCU port pin order
	while (chunk_vectors_count--) {
		// convert received vector bytes into a temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<dut_pin_count ; i+=8, vector_slice++) {
			bitvector |= (uint32_t) *vector_slice << i;
		}

		// clear current vector data
		for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) v->port[i].out = 0;
		v->check = 1;

		// fill in bits in MCU port pin order
		for (uint8_t dut_pin=0 ; dut_pin<dut_pin_count ; dut_pin++) {
			uint8_t zif_pin = zif_pos(dut_pin_count, dut_pin);
			int8_t port_pos = zif_mcu_port(zif_pin);
			uint8_t bit_val = (bitvector >> dut_pin) & 1;
			if ((zif_pin == zif_vcc_pin) && bit_val) {
				v->check = 0;
			} else {
				v->port[port_pos].out |= bit_val << zif_mcu_port_bit(zif_pin);
			}
		}
		v++;
	}

	return RESP_OK;
}

// -----------------------------------------------------------------------
static uint8_t handle_failure(uint16_t pos, struct mcu_port_config *mcu_port)
{
	// Retest current vector after 5us.
	// If it passes this time, it's a test timing error, not a failed IC.
	_delay_us(5);

	// store failed vector for the response data
	failed_vector_pos = pos;
	failed_vector[ZIF_PORT_0] = ZIF_MCU_PIN_0;
	failed_vector[ZIF_PORT_1] = ZIF_MCU_PIN_1;
	failed_vector[ZIF_PORT_2] = ZIF_MCU_PIN_2;

	if ((failed_vector[ZIF_PORT_0] & mcu_port[ZIF_PORT_0].mask) != vectors[pos].port[ZIF_PORT_0].out) return RESP_FAIL;
	if ((failed_vector[ZIF_PORT_1] & mcu_port[ZIF_PORT_1].mask) != vectors[pos].port[ZIF_PORT_1].out) return RESP_FAIL;
	if ((failed_vector[ZIF_PORT_2] & mcu_port[ZIF_PORT_2].mask) != vectors[pos].port[ZIF_PORT_2].out) return RESP_FAIL;

	return RESP_TIMING_ERROR;
}

// -----------------------------------------------------------------------
static inline uint8_t logic_run_2port(struct mcu_port_config *mcu_port)
{
	uint16_t local_delay = delay; // need to trick the optimizer :-(
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		ZIF_MCU_PORT_0 = vectors[pos].port[ZIF_PORT_0].in;
		ZIF_MCU_PORT_2 = vectors[pos].port[ZIF_PORT_2].in;

		if (!vectors[pos].check) continue;
		if (local_delay) _delay_loop_2(local_delay);

		if ((ZIF_MCU_PIN_0 & mcu_port[ZIF_PORT_0].mask) != vectors[pos].port[ZIF_PORT_0].out) return handle_failure(pos, mcu_port);
		if ((ZIF_MCU_PIN_2 & mcu_port[ZIF_PORT_2].mask) != vectors[pos].port[ZIF_PORT_2].out) return handle_failure(pos, mcu_port);
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t logic_run_3port(struct mcu_port_config *mcu_port)
{
	uint16_t local_delay = delay; // need to trick the optimizer :-(
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		ZIF_MCU_PORT_0 = vectors[pos].port[ZIF_PORT_0].in;
		ZIF_MCU_PORT_1 = vectors[pos].port[ZIF_PORT_1].in;
		ZIF_MCU_PORT_2 = vectors[pos].port[ZIF_PORT_2].in;

		if (!vectors[pos].check) continue;
		if (local_delay) _delay_loop_2(local_delay);

		if ((ZIF_MCU_PIN_0 & mcu_port[ZIF_PORT_0].mask) != vectors[pos].port[ZIF_PORT_0].out) return handle_failure(pos, mcu_port);
		if ((ZIF_MCU_PIN_1 & mcu_port[ZIF_PORT_1].mask) != vectors[pos].port[ZIF_PORT_1].out) return handle_failure(pos, mcu_port);
		if ((ZIF_MCU_PIN_2 & mcu_port[ZIF_PORT_2].mask) != vectors[pos].port[ZIF_PORT_2].out) return handle_failure(pos, mcu_port);
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
void logic_imeasure(uint8_t dut_pin_count)
{
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		ZIF_MCU_PORT_0 = vectors[pos].port[ZIF_PORT_0].in;
		ZIF_MCU_PORT_1 = vectors[pos].port[ZIF_PORT_1].in;
		if (dut_pin_count <= 16) {
			ZIF_MCU_PORT_2 = vectors[pos].port[ZIF_PORT_2].in;
		}

		update_current_stats();
	}
}

// -----------------------------------------------------------------------
uint8_t logic_run(uint8_t dut_pin_count, uint16_t loops)
{
	uint8_t res;

	// local copy for speed (pointer known at compile time)
	struct mcu_port_config mcu_port_copy[MCU_PORT_CNT];
	struct mcu_port_config *mcu_port = mcu_get_port_config();
	if (!mcu_port) {
		return error(ERR_NO_PINCFG);
	}
	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) mcu_port_copy[i] = mcu_port[i];

	if (!vectors_count) {
		return error(ERR_VECT_NUM);
	}

	// precompute input/output vectors with port masks
	for (uint16_t pos=0 ; pos<vectors_count ; pos++) {
		for (uint8_t port=0 ; port<MCU_PORT_CNT ; port++) {
			vectors[pos].port[port].in = (vectors[pos].port[port].out & mcu_port[port].output) | mcu_port[port].pullup;
			vectors[pos].port[port].out &= mcu_port[port].mask;
		}
	}

	logic_imeasure(dut_pin_count);

	if (dut_pin_count <= 16) {
		for (rep=0 ; rep<loops ; rep++) {
			if ((res = logic_run_2port(mcu_port_copy)) != RESP_PASS) return res;
		}
	} else {
		for (rep=0 ; rep<loops ; rep++) {
			if ((res = logic_run_3port(mcu_port_copy)) != RESP_PASS) return res;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint16_t logic_store_result(uint8_t *buf, uint8_t dut_pin_count)
{
	struct resp_logic_fail *resp = (struct resp_logic_fail*) buf;
	resp->loop_num = rep;
	resp->vector_num = failed_vector_pos;

	for (uint8_t i=0 ; i<3 ; i++) resp->vector[i] = 0;

	// translate vector from MCU port order to natural DUT pin order
	for (uint8_t pin=0 ; pin<dut_pin_count ; pin++) {
		uint8_t zif_pin = zif_pos(dut_pin_count, pin);
		uint8_t mcu_port = zif_mcu_port(zif_pin);
		uint8_t mcu_port_bit = zif_mcu_port_bit(zif_pin);
		bool bit = failed_vector[mcu_port] & _BV(mcu_port_bit);
		resp->vector[pin / 8] |= bit << (pin % 8);
	}

	uint16_t count = 6;
	if (dut_pin_count > 16) count += 1;

	return count;
}

// vim: tabstop=4 shiftwidth=4 autoindent
