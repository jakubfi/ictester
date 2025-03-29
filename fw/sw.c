#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>
#include <util/delay.h>

#include "external/fleury-i2cmaster/i2cmaster_a.h"
#include "external/fleury-i2cmaster/i2cmaster_b.h"

#include "protocol.h"
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
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x98, 0b00000000}, // A0
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9a, 0b10001001}, // A1
	{i2c_a_start_wait, i2c_a_stop, i2c_a_write, 0x9c, 0b00000010}, // A2
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x98, 0b00101001}, // B0
	{i2c_b_start_wait, i2c_b_stop, i2c_b_write, 0x9c, 0b00000000}, // B1 (i2c address is 2 instead of 1)
};

uint8_t switch_config[MAX_CONFIGS][SWITCH_CNT];
uint8_t *switch_config_active;

// -----------------------------------------------------------------------
void sw_init()
{
	i2c_a_init();
	i2c_b_init();
	sw_config_clear();
	switch_config_active = NULL;
}

// -----------------------------------------------------------------------
void sw_config_select(uint8_t cfgnum)
{
	switch_config_active = switch_config[cfgnum];
}

// -----------------------------------------------------------------------
void sw_on(uint8_t port, uint8_t bit)
{
	switch_config_active[port] |= _BV(bit);
}

// -----------------------------------------------------------------------
bool sw_config_sane()
{
	if ((switch_config_active[A1] & 0b00001010) == 0b00001010) return false; // pin 8 VCC+GND
	if ((switch_config_active[B0] & 0b00000011) == 0b00000011) return false; // pin 24 VCC+GND
	// check for disallowed inter-config changes
	return true;
}

// -----------------------------------------------------------------------
void sw_push_config(uint8_t cfg)
{
	const __flash struct switch_drv *sw = zif_switch;
	for (uint8_t i=0 ; i<SWITCH_CNT ; i++, sw++) {
		sw->i2c_start_wait(sw->i2c_addr);
		sw->i2c_write(0);
		if (cfg == SW_CFG_GND_ONLY) sw->i2c_write(switch_config_active[i] & sw->gnd_mask);
		else sw->i2c_write(switch_config_active[i]);
		sw->i2c_stop();
	}
}

// -----------------------------------------------------------------------
bool sw_connect()
{
	if (!switch_config_active) {
		error(ERR_NO_PINCFG);
		return false;
	}

	if (!sw_config_sane()) {
		error(ERR_PIN_COMB);
		return false;
	}

	// connect grounds first
	sw_push_config(SW_CFG_GND_ONLY);
	sw_push_config(SW_CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);

	return true;
}

// -----------------------------------------------------------------------
void sw_config_clear()
{
	for (uint8_t cfgnum=0 ; cfgnum<MAX_CONFIGS ; cfgnum++) {
		for (uint8_t i=0 ; i<SWITCH_CNT ; i++) {
			switch_config[cfgnum][i] = 0;
		}
	}
}

// -----------------------------------------------------------------------
void sw_disconnect()
{
	if (!switch_config_active) return;

	// disconnect grounds last
	sw_push_config(SW_CFG_GND_ONLY);
	sw_config_clear();
	sw_push_config(SW_CFG_ALL);
	_delay_us(SWITCH_ON_DELAY_US);
	switch_config_active = NULL;
}

// vim: tabstop=4 shiftwidth=4 autoindent
