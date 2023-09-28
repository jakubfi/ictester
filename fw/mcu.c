#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include "protocol.h"
#include "mcu.h"

#define NO_CONFIG -1

struct mcu_port_config mcu_port[MAX_CONFIGS][MCU_PORT_CNT];
struct mcu_port_config *mcu_config;

// -----------------------------------------------------------------------
void mcu_init()
{
	mcu_config_clear();
	mcu_config = NULL;
}

// -----------------------------------------------------------------------
void mcu_config_select(uint8_t cfgnum)
{
	mcu_config = mcu_port[cfgnum];
}

// -----------------------------------------------------------------------
void mcu_disconnect()
{   
	DDRA = 0;
	PORTA = 0;
	DDRB = 0;
	PORTB = 0;
	DDRC = 0;
	PORTC = 0;
	mcu_config = NULL;
}	   

// -----------------------------------------------------------------------
bool mcu_connect()
{
	if (!mcu_config) {
		error(ERR_NO_PINCFG);
		return false;
	}

	DDRA  = mcu_config[PA].output;
	DDRB  = mcu_config[PB].output;
	DDRC  = mcu_config[PC].output;
	PORTA = mcu_config[PA].pullup;
	PORTB = mcu_config[PB].pullup;
	PORTC = mcu_config[PC].pullup;

	return true;
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
bool mcu_func(uint8_t func, uint8_t port_pos, uint8_t port_bit)
{
	if (!mcu_config) {
		error(ERR_NO_PINCFG);
		return false;
	}

	switch (func) {
		case ZIF_OUT:
			mcu_config[port_pos].output |= _BV(port_bit);
			break;
		case ZIF_IN_PU_WEAK:
			mcu_config[port_pos].pullup |= _BV(port_bit);
			[[ fallthrough ]];
		case ZIF_IN_HIZ:
		case ZIF_IN_PU_STRONG:
			mcu_config[port_pos].input |= _BV(port_bit);
			break;
		default:
			error(ERR_PIN_FUNC);
			return false;
	}

	return true;
}

// -----------------------------------------------------------------------
struct mcu_port_config * mcu_get_port_config()
{
	return mcu_config;
}

// vim: tabstop=4 shiftwidth=4 autoindent
