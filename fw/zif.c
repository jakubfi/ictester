#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>

#include "protocol.h"
#include "sw.h"

#define ZIF_PIN_CNT 24

#define PA 0 // MCU port A
#define PB 1 // MCU port B
#define PC 2 // MCU port C

// Generic port/bit coordinates
struct coord {
	int8_t port : 4;
	int8_t bit : 4;
};

// translates ZIF pin (0-based) number to MCU port/bit
const __flash struct coord zif_pin_to_mcu[ZIF_PIN_CNT] = {
	{PC, 0}, {PC, 1}, {PC, 2}, {PC, 3}, {PC, 4}, {PC, 5}, {PC, 6}, {PC, 7}, {PA, 7}, {PA, 6}, {PA, 5}, {PA, 4},
	{PA, 3}, {PA, 2}, {PA, 1}, {PA, 0}, {PB, 0}, {PB, 1}, {PB, 2}, {PB, 3}, {PB, 4}, {PB, 5}, {PB, 6}, {PB, 7}
};

// Translates ZIF pin (0-based) number to SW port/bit for each function available
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
void zif_init(void)
{
	sw_init();
}

// -----------------------------------------------------------------------
uint8_t zif_pos(uint8_t dut_dut_pin_count, uint8_t dut_pin)
{
    return dut_pin < (dut_dut_pin_count/2) ? dut_pin : ZIF_PIN_CNT-dut_dut_pin_count + dut_pin;
}

// -----------------------------------------------------------------------
bool zif_func(uint8_t func, uint8_t pin)
{
	const __flash struct coord *coord;

	switch (func) {
		case ZIF_VCC:
			coord = zif_vcc_coord;
			break;
		case ZIF_GND:
			coord = zif_gnd_coord;
			break;
		case ZIF_IN_PU_STRONG:
			coord = zif_pu_coord;
			break;
		case ZIF_C:
			coord = zif_c_coord;
			break;
		default:
			return false;
	}
	coord += pin;

	if (coord->port == NA) return false;

	sw_on(coord->port, coord->bit);

	return true;
}

// -----------------------------------------------------------------------
bool zif_config_sane(void)
{
	return sw_config_sane();
}

// -----------------------------------------------------------------------
void zif_connect(void)
{
	sw_connect();
}

// -----------------------------------------------------------------------
void zif_disconnect(void)
{
	sw_disconnect();
}

// -----------------------------------------------------------------------
uint8_t get_mcu_port(uint8_t zif_pin)
{
	return zif_pin_to_mcu[zif_pin].port;
}

// -----------------------------------------------------------------------
uint8_t get_mcu_port_bit(uint8_t zif_pin)
{
	return zif_pin_to_mcu[zif_pin].bit;
}

// vim: tabstop=4 shiftwidth=4 autoindent
