#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>
#include <util/delay.h>

#include "external/fleury-i2cmaster/i2cmaster_a.h"
#include "external/fleury-i2cmaster/i2cmaster_b.h"

#include "protocol.h"

#define ZIF_PIN_CNT 24
#define SWITCH_CNT 5

#define CFG_ALL 0
#define CFG_GND_ONLY 1

// switch turn-on time @3.3V from datasheet, probably even less for 5V
#define SWITCH_ON_DELAY_US 35

#define A0 0 // analog switch 0, I2C bus A (top left)
#define A1 1 // analog switch 1, I2C bus A
#define A2 2 // analog switch 2, I2C bus A
#define B0 3 // analog switch 0, I2C bus B (top right)
#define B1 4 // analog switch 1, I2C bus B
#define NA -1 // not connected

#define PA 0 // MCU port A
#define PB 1 // MCU port B
#define PC 2 // MCU port C

// MCU ports mapping and configuration

struct pin_coord {
	int8_t port;
	int8_t pin;
} pin_coord;

const __flash struct pin_coord zif_pin_coord[ZIF_PIN_CNT] = {
	{PC, 0}, {PC, 1}, {PC, 2}, {PC, 3}, {PC, 4}, {PC, 5}, {PC, 6}, {PC, 7}, {PA, 7}, {PA, 6}, {PA, 5}, {PA, 4},
	{PA, 3}, {PA, 2}, {PA, 1}, {PA, 0}, {PB, 0}, {PB, 1}, {PB, 2}, {PB, 3}, {PB, 4}, {PB, 5}, {PB, 6}, {PB, 7}
};

// Analog switches mapping and configuration

struct switch_coord {
    int8_t addr;
    int8_t pos;
} switch_coord;

const __flash struct switch_drv {
	void (*i2c_start_wait)(unsigned char);
	void (*i2c_stop)(void);
	unsigned char (*i2c_write)(unsigned char);
	uint8_t i2c_addr;
	uint8_t gnd_mask;
} zif_switch[SWITCH_CNT] = {
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x98, 0b00000001}, // A0
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9a, 0b00011000}, // A1
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9c, 0b00001001}, // A2
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x98, 0b01000100}, // B0
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x9a, 0b00100000}, // B1
};

uint8_t switch_data[SWITCH_CNT] = {0, 0, 0, 0, 0};

const __flash struct switch_coord zif_vcc_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {A0, 5},  {A0, 7},  {NA, NA}, {NA, NA}, {A1, 2},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B0, 1}
};

const __flash struct switch_coord zif_gnd_coord[ZIF_PIN_CNT] = {
	{A0, 0},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 4},  {A1, 3},  {NA, NA}, {A2, 3},  {NA, NA}, {A2, 0},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 5},  {B0, 6},  {NA, NA}, {NA, NA}, {B0, 2}
};

const __flash struct switch_coord zif_pu_coord[ZIF_PIN_CNT] = {
	{A0, 1},  {A0, 2},  {A0, 3},  {A0, 4},  {A0, 6},  {A1, 7},  {A1, 5},  {A1, 1},  {A1, 0},  {A2, 4},  {A2, 2},  {A2, 1},
	{A2, 7},  {A2, 6},  {A2, 5},  {B1, 0},  {B1, 1},  {B1, 2},  {B1, 3},  {B1, 4},  {B1, 7},  {B0, 5},  {B0, 3},  {B0, 0}
};

const __flash struct switch_coord zif_c_coord[ZIF_PIN_CNT] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 6},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 6},  {B0, 7},  {B0, 4},  {NA, NA}, {NA, NA}
};


// -----------------------------------------------------------------------
void zif_init(void)
{
	i2c_a_init();
	i2c_b_init();
}

// -----------------------------------------------------------------------
uint8_t zif_pos(uint8_t dut_pin_count, uint8_t dut_pin)
{
    return dut_pin < (dut_pin_count/2) ? dut_pin : ZIF_PIN_CNT-dut_pin_count + dut_pin;
}

// -----------------------------------------------------------------------
bool zif_func(uint8_t func, uint8_t pin)
{
	const __flash struct switch_coord *coord;

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

	if (coord->addr == NA) return false;

	switch_data[coord->addr] |= 1 << coord->pos;

	return true;
}

// -----------------------------------------------------------------------
bool zif_config_sane(void)
{
	if ((switch_data[A1] & 0b00001100) == 0b00001100) return false; // pin 8 VCC+GND
	if ((switch_data[B0] & 0b00000110) == 0b00000110) return false; // pin 24 VCC+GND
	// TODO: GND + pullup?
	// TODO: C + no pullup
	// TODO: VCC + pullup?
	// TODO: or just any two functions?
	// TODO: more than one GND/VCC/C?
	return true;
}

// -----------------------------------------------------------------------
static void zif_push_config(uint8_t cfg)
{
	const __flash struct switch_drv *sw = zif_switch;
	for (uint8_t i=0 ; i<SWITCH_CNT ; i++, sw++) {
		sw->i2c_start_wait(sw->i2c_addr);
		sw->i2c_write(0);
		if (cfg == CFG_GND_ONLY) sw->i2c_write(switch_data[i] & sw->gnd_mask);
		else sw->i2c_write(switch_data[i]);
		sw->i2c_stop();
	}
}

// -----------------------------------------------------------------------
void zif_connect(void)
{
	// connect grounds first
	zif_push_config(CFG_GND_ONLY);
	zif_push_config(CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);
}

// -----------------------------------------------------------------------
void zif_disconnect(void)
{
	// disconnect grouds last
	zif_push_config(CFG_GND_ONLY);
	for (uint8_t i=0 ; i<SWITCH_CNT ; i++) switch_data[i] = 0;
	zif_push_config(CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);
}

// -----------------------------------------------------------------------
uint8_t mcu_port(uint8_t zif_pin)
{
	return zif_pin_coord[zif_pin].port;
}

// -----------------------------------------------------------------------
uint8_t mcu_port_pin(uint8_t zif_pin)
{
	return zif_pin_coord[zif_pin].pin;
}

// vim: tabstop=4 shiftwidth=4 autoindent
