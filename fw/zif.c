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
	const uint8_t port : 4;
	const uint8_t bit : 4;
};

// Translates ZIF pin number (0-based) to MCU port/bit
static const __flash struct coord zif_pin_to_mcu[ZIF_PIN_CNT] = {
	{ZIF_PORT_0, ZIF_0_PORT_BIT},
	{ZIF_PORT_0, ZIF_1_PORT_BIT},
	{ZIF_PORT_0, ZIF_2_PORT_BIT},
	{ZIF_PORT_0, ZIF_3_PORT_BIT},
	{ZIF_PORT_0, ZIF_4_PORT_BIT},
	{ZIF_PORT_0, ZIF_5_PORT_BIT},
	{ZIF_PORT_0, ZIF_6_PORT_BIT},
	{ZIF_PORT_0, ZIF_7_PORT_BIT},
	{ZIF_PORT_1, ZIF_8_PORT_BIT},
	{ZIF_PORT_1, ZIF_9_PORT_BIT},
	{ZIF_PORT_1, ZIF_10_PORT_BIT},
	{ZIF_PORT_1, ZIF_11_PORT_BIT},
	{ZIF_PORT_1, ZIF_12_PORT_BIT},
	{ZIF_PORT_1, ZIF_13_PORT_BIT},
	{ZIF_PORT_1, ZIF_14_PORT_BIT},
	{ZIF_PORT_1, ZIF_15_PORT_BIT},
	{ZIF_PORT_2, ZIF_16_PORT_BIT},
	{ZIF_PORT_2, ZIF_17_PORT_BIT},
	{ZIF_PORT_2, ZIF_18_PORT_BIT},
	{ZIF_PORT_2, ZIF_19_PORT_BIT},
	{ZIF_PORT_2, ZIF_20_PORT_BIT},
	{ZIF_PORT_2, ZIF_21_PORT_BIT},
	{ZIF_PORT_2, ZIF_22_PORT_BIT},
	{ZIF_PORT_2, ZIF_23_PORT_BIT}
};

// Translates ZIF pin number (0-based) to SW port/bit for each function available
static const __flash struct coord zif_vcc_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {A0, 4},  {A0, 5},  {NA, NA}, {NA, NA}, {A1, 1},  {A1,  5}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B0, 1}
};

static const __flash struct coord zif_gnd_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 0},  {A1, 3},  {NA, NA}, {A1, 7},  {NA, NA}, {A2, 1},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B0, 5},  {B0, 3},  {NA, NA}, {NA, NA}, {B0, 0}
};

static const __flash struct coord zif_pu_coord[ZIF_PIN_CNT] = {
	{A0, 0},  {A0, 1},  {A0, 2},  {A0, 3},  {A0, 6},  {A0, 7},  {B1, 7},  {A1, 2},  {A1, 4},  {A1, 6},  {A2, 2},  {A2, 0},
	{A2, 7},  {A2, 6},  {A2, 5},  {A2, 4},  {A2, 3},  {B0, 7},  {B0, 6},  {B0, 4},  {B1, 4},  {B1, 2},  {B1, 0},  {B0, 2}
};

static const __flash struct coord zif_c_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 6},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 5},  {B1, 3},  {B1, 1},  {NA, NA}, {NA, NA}
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
