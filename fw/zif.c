#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>

#include "protocol.h"
#include "zif.h"
#include "sw.h"
#include "mcu.h"

uint8_t zif_vcc_pin;

// Generic port/bit coordinates
struct coord {
	uint8_t port : 4;
	uint8_t bit : 4;
};

// Translates ZIF pin number (0-based) to MCU port/bit
const __flash struct coord zif_pin_to_mcu[ZIF_PIN_CNT] = {
	{PC, 0}, {PC, 1}, {PC, 2}, {PC, 3}, {PC, 4}, {PC, 5}, {PC, 6}, {PC, 7}, {PA, 7}, {PA, 6}, {PA, 5}, {PA, 4},
	{PA, 3}, {PA, 2}, {PA, 1}, {PA, 0}, {PB, 0}, {PB, 1}, {PB, 2}, {PB, 3}, {PB, 4}, {PB, 5}, {PB, 6}, {PB, 7}
};

// Translates ZIF pin number (0-based) to SW port/bit for each function available
const __flash struct coord zif_vcc_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {A0, 5},  {A0, 7},  {NA, NA}, {NA, NA}, {A1, 2},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B0, 1}
};

const __flash struct coord zif_gnd_coord[ZIF_PIN_CNT] = {
	{A0, 0},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 4},  {A1, 3},  {NA, NA}, {A2, 3},  {NA, NA}, {A2, 0},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 5},  {B0, 6},  {NA, NA}, {NA, NA}, {B0, 2}
};

const __flash struct coord zif_pu_coord[ZIF_PIN_CNT] = {
	{A0, 1},  {A0, 2},  {A0, 3},  {A0, 4},  {A0, 6},  {A1, 7},  {A1, 5},  {A1, 1},  {A1, 0},  {A2, 4},  {A2, 2},  {A2, 1},
	{A2, 7},  {A2, 6},  {A2, 5},  {B1, 0},  {B1, 1},  {B1, 2},  {B1, 3},  {B1, 4},  {B1, 7},  {B0, 5},  {B0, 3},  {B0, 0}
};

const __flash struct coord zif_c_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 6},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 6},  {B0, 7},  {B0, 4},  {NA, NA}, {NA, NA}
};

// -----------------------------------------------------------------------
void zif_init()
{
	sw_init();
	mcu_init();
}

// -----------------------------------------------------------------------
void zif_config_clear()
{
	mcu_config_clear();
	sw_config_clear();
}

// -----------------------------------------------------------------------
void zif_config_select(uint8_t cfgnum)
{
	// check if cfgnum is actually present
	mcu_config_select(cfgnum);
	sw_config_select(cfgnum);
}

// -----------------------------------------------------------------------
uint8_t zif_pos(uint8_t dut_pin_count, uint8_t dut_pin)
{
	return dut_pin < (dut_pin_count/2) ? dut_pin : ZIF_PIN_CNT-dut_pin_count + dut_pin;
}

// -----------------------------------------------------------------------
uint8_t zif_mcu_port(uint8_t zif_pin)
{
	return zif_pin_to_mcu[zif_pin].port;
}

// -----------------------------------------------------------------------
uint8_t zif_mcu_port_bit(uint8_t zif_pin)
{
	return zif_pin_to_mcu[zif_pin].bit;
}

// -----------------------------------------------------------------------
bool zif_func(uint8_t func, uint8_t zif_pin)
{
	uint8_t port_pos, port_bit;
	const __flash struct coord *coord = NULL;

	switch (func) {
		case ZIF_IN_PU_STRONG:
			coord = zif_pu_coord + zif_pin;
			 [[ fallthrough ]];
		case ZIF_IN_PU_WEAK:
		case ZIF_OUT:
		case ZIF_IN_HIZ:
			port_pos = zif_mcu_port(zif_pin);
			port_bit = zif_mcu_port_bit(zif_pin);
			if (!mcu_func(func, port_pos, port_bit)) {
				return false; // cause set downstream
			}
			break;
		case ZIF_VCC:
			zif_vcc_pin = zif_pin;
			coord = zif_vcc_coord + zif_pin;
			break;
		case ZIF_GND:
			coord = zif_gnd_coord + zif_pin;
			break;
		case ZIF_C:
			coord = zif_c_coord + zif_pin;
			break;
		default:
			error(ERR_PIN_FUNC);
			return false;
	}

	if (coord) { // SW function
		if (coord->port == NA) {
			error(ERR_PIN_FUNC_UNAVAILABLE);
			return false;
		}
		sw_on(coord->port, coord->bit);
	}

	return true;
}

// -----------------------------------------------------------------------
bool zif_connect()
{
	if (!sw_connect()) {
		return false; // error set downstream
	}
	if (!mcu_connect()) {
		return false; // error set downstream
	}
	return true;
}

// -----------------------------------------------------------------------
void zif_disconnect()
{
	mcu_disconnect();
	sw_disconnect();
}

// -----------------------------------------------------------------------
uint8_t zif_get_vcc_pin()
{
	return zif_vcc_pin;
}

// vim: tabstop=4 shiftwidth=4 autoindent
