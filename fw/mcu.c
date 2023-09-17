#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include "protocol.h"
#include "mcu.h"

#define NO_CONFIG -1

struct mcu_port_config mcu_port[MAX_CONFIGS][MCU_PORT_CNT];
uint8_t current_config;

// -----------------------------------------------------------------------
void mcu_disconnect()
{   
	DDRA = 0;
	PORTA = 0;
	DDRB = 0;
	PORTB = 0;
	DDRC = 0;
	PORTC = 0;
	current_config = NO_CONFIG;
}	   

// -----------------------------------------------------------------------
void mcu_connect(uint8_t cfgnum)
{
	current_config = cfgnum;
	DDRA  = mcu_port[cfgnum][PA].output;
	DDRB  = mcu_port[cfgnum][PB].output;
	DDRC  = mcu_port[cfgnum][PC].output;
	PORTA = mcu_port[cfgnum][PA].pullup;
	PORTB = mcu_port[cfgnum][PB].pullup;
	PORTC = mcu_port[cfgnum][PC].pullup;
}

// -----------------------------------------------------------------------
void mcu_config_clear()
{
	for (uint8_t cfgnum=0 ; cfgnum<MAX_CONFIGS ; cfgnum++) {
		for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
			mcu_port[cfgnum][i].input = 0;
			mcu_port[cfgnum][i].output = 0;
			mcu_port[cfgnum][i].pullup = 0;
		}
	}
}

// -----------------------------------------------------------------------
void mcu_pin_mask_clear(uint8_t cfgnum)
{
	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
		mcu_port[cfgnum][i].mask = 0;
	}
}

// -----------------------------------------------------------------------
void mcu_init()
{
	mcu_config_clear();
}

// -----------------------------------------------------------------------
bool mcu_func(uint8_t cfgnum, uint8_t func, uint8_t port_pos, uint8_t port_bit)
{
	switch (func) {
		case ZIF_OUT:
			mcu_port[cfgnum][port_pos].output |= _BV(port_bit);
			break;
		case ZIF_IN_HIZ:
			mcu_port[cfgnum][port_pos].input |= _BV(port_bit);
			break;
		case ZIF_IN_PU_WEAK:
			mcu_port[cfgnum][port_pos].input |= _BV(port_bit);
			mcu_port[cfgnum][port_pos].pullup |= _BV(port_bit);
			break;
		case ZIF_IN_PU_STRONG:
			mcu_port[cfgnum][port_pos].input |= _BV(port_bit);
			break;
		default:
			return false;
	}

	return true;
}

// -----------------------------------------------------------------------
void mcu_pin_unmasked(uint8_t cfgnum, uint8_t port_pos, uint8_t port_bit)
{
	mcu_port[cfgnum][port_pos].mask |= mcu_port[cfgnum][port_pos].input & _BV(port_bit);
}

// -----------------------------------------------------------------------
struct mcu_port_config * mcu_get_port_config()
{
	if (current_config == NO_CONFIG) return NULL;
	return mcu_port[current_config];
}

// vim: tabstop=4 shiftwidth=4 autoindent
