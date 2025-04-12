#include <stdbool.h>
#include <stdlib.h>
#include <avr/io.h>
#include <util/delay.h>

#include "protocol.h"
#include "mcu.h"
#include "zif.h"

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
void mcu_deconfigure()
{   
	ZIF_MCU_DDR_0 = 0;
	ZIF_MCU_PORT_0 = 0;
	ZIF_MCU_DDR_1 = 0;
	ZIF_MCU_PORT_1 = 0;
	ZIF_MCU_DDR_2 = 0;
	ZIF_MCU_PORT_2 = 0;
	mcu_config = NULL;
}	   

// -----------------------------------------------------------------------
void mcu_drain_pins()
{
	ZIF_MCU_DDR_0 = 0xff;
	ZIF_MCU_PORT_0 = 0;
	ZIF_MCU_DDR_1 = 0xff;
	ZIF_MCU_PORT_1 = 0;
	ZIF_MCU_DDR_2 = 0xff;
	ZIF_MCU_PORT_2 = 0;
	_delay_ms(3);
}

// -----------------------------------------------------------------------
bool mcu_connect()
{
	if (!mcu_config) {
		error(ERR_NO_PINCFG);
		return false;
	}

	ZIF_MCU_DDR_0 = mcu_config[ZIF_PORT_0].output;
	ZIF_MCU_DDR_1 = mcu_config[ZIF_PORT_1].output;
	ZIF_MCU_DDR_2 = mcu_config[ZIF_PORT_2].output;
	ZIF_MCU_PORT_0 = mcu_config[ZIF_PORT_0].pullup;
	ZIF_MCU_PORT_1 = mcu_config[ZIF_PORT_1].pullup;
	ZIF_MCU_PORT_2 = mcu_config[ZIF_PORT_2].pullup;

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
