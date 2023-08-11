#include <inttypes.h>
#include <stdbool.h>
#include <util/delay.h>

#include "external/fleury-i2cmaster/i2cmaster_a.h"
#include "external/fleury-i2cmaster/i2cmaster_b.h"

#include "protocol.h"

#define A0 0 // sw 0, bus A
#define A1 1 // sw 1, bus A
#define A2 2 // sw 2, bus A
#define B0 3 // sw 0, bus B
#define B1 4 // sw 1, bus B
#define NA -1 // not connected

#define PA 0 // MCU port A
#define PB 1 // MCU port B
#define PC 2 // MCU port C

// MCU ports mapping and configuration

struct pin_coord {
	int8_t port;
	int8_t pin;
} pin_coord;

const __flash struct pin_coord zif_pin_coord[24] = {
	{PC, 0}, {PC, 1}, {PC, 2}, {PC, 3}, {PC, 4}, {PC, 5}, {PC, 6}, {PC, 7}, {PA, 7}, {PA, 6}, {PA, 5}, {PA, 4},
	{PA, 3}, {PA, 2}, {PA, 1}, {PA, 0}, {PB, 0}, {PB, 1}, {PB, 2}, {PB, 3}, {PB, 4}, {PB, 5}, {PB, 6}, {PB, 7}
};

// Analog switches mapping and configuration

struct switch_coord {
    int8_t addr;
    int8_t pos;
} switch_coord;

struct switch_drv {
	void (*i2c_start_wait)(unsigned char);
	void (*i2c_stop)(void);
	unsigned char (*i2c_write)(unsigned char);
	uint8_t i2c_addr;
	uint8_t data;
} zif_switch[5] = {
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x98, 0}, // A0
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9a, 0}, // A1
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9c, 0}, // A2
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x98, 0}, // B0
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x9a, 0}, // B1
};

const __flash struct switch_coord zif_vcc_coord[24] = {
	{NA, NA}, {NA, NA}, {NA, NA}, {A0, 5},  {A0, 7},  {NA, NA}, {NA, NA}, {A1, 2},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B0, 1}
};

const __flash struct switch_coord zif_gnd_coord[24] = {
	{A0, 0},  {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {A1, 4},  {A1, 3},  {NA, NA}, {A2, 3},  {NA, NA}, {A2, 0},
	{NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {NA, NA}, {B1, 5},  {B0, 6},  {NA, NA}, {NA, NA}, {B0, 2}
};

const __flash struct switch_coord zif_pu_coord[24] = {
	{A0, 1},  {A0, 2},  {A0, 3},  {A0, 4},  {A0, 6},  {A1, 7},  {A1, 5},  {A1, 1},  {A1, 0},  {A2, 4},  {A2, 2},  {A2, 1},
	{A2, 7},  {A2, 6},  {A2, 5},  {B1, 0},  {B1, 1},  {B1, 2},  {B1, 3},  {B1, 4},  {B1, 7},  {B0, 5},  {B0, 3},  {B0, 0}
};

const __flash struct switch_coord zif_c_coord[24] = {
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
    return dut_pin < (dut_pin_count/2) ? dut_pin : 24-dut_pin_count + dut_pin;
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

	zif_switch[coord->addr].data |= 1 << coord->pos;

	return true;
}

// -----------------------------------------------------------------------
static bool zif_config_sane(void)
{
	if ((zif_switch[A1].data & 0b00001100) == 0b00001100) return false; // pin 8 VCC+GND
	if ((zif_switch[B0].data & 0b00000110) == 0b00000110) return false; // pin 24 VCC+GND
	// TODO: GND + pullup?
	// TODO: C + no pullup
	// TODO: VCC + pullup?
	// TODO: or just any two functions?
	return true;
}

// -----------------------------------------------------------------------
static void zif_push_config(void)
{
	for (uint8_t i=0 ; i<5 ; i++) {
		struct switch_drv *sw = zif_switch+i;
		sw->i2c_start_wait(sw->i2c_addr);
		sw->i2c_write(0);
		sw->i2c_write(sw->data);
		sw->i2c_stop();
	}
	_delay_us(35); // turn-on time @3.3v from datasheet
}

// -----------------------------------------------------------------------
bool zif_connect(void)
{
	if (!zif_config_sane()) return false;

	zif_push_config();

	return true;
}

// -----------------------------------------------------------------------
void zif_disconnect(void)
{
	for (uint8_t i=0 ; i<5 ; i++) {
		zif_switch[i].data = 0;
	}
	zif_push_config();
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
