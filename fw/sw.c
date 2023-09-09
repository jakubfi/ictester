#include <inttypes.h>
#include <stdbool.h>
#include <util/delay.h>

#include "external/fleury-i2cmaster/i2cmaster_a.h"
#include "external/fleury-i2cmaster/i2cmaster_b.h"

#include "sw.h"

#define SWITCH_CNT 5

// switch turn-on time @3.3V from datasheet, probably even less for 5V
#define SWITCH_ON_DELAY_US 35

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

uint8_t switch_data[SWITCH_CNT];

// -----------------------------------------------------------------------
void sw_init()
{
	i2c_a_init();
	i2c_b_init();
	sw_config_clear();
}

// -----------------------------------------------------------------------
void sw_on(uint8_t port, uint8_t bit)
{
	switch_data[port] |= _BV(bit);
}

// -----------------------------------------------------------------------
bool sw_config_sane()
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
void sw_push_config(uint8_t cfg)
{
	const __flash struct switch_drv *sw = zif_switch;
	for (uint8_t i=0 ; i<SWITCH_CNT ; i++, sw++) {
		sw->i2c_start_wait(sw->i2c_addr);
		sw->i2c_write(0);
		if (cfg == SW_CFG_GND_ONLY) sw->i2c_write(switch_data[i] & sw->gnd_mask);
		else sw->i2c_write(switch_data[i]);
		sw->i2c_stop();
	}
}

// -----------------------------------------------------------------------
void sw_connect()
{
	// connect grounds first
	sw_push_config(SW_CFG_GND_ONLY);
	sw_push_config(SW_CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);
}

// -----------------------------------------------------------------------
void sw_config_clear()
{
	for (uint8_t i=0 ; i<SWITCH_CNT ; i++) switch_data[i] = 0;
}

// -----------------------------------------------------------------------
void sw_disconnect()
{
	// disconnect grouds last
	sw_push_config(SW_CFG_GND_ONLY);
	sw_config_clear();
	sw_push_config(SW_CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);
}

// vim: tabstop=4 shiftwidth=4 autoindent
