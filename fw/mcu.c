#include <stdbool.h>
#include <avr/io.h>
#include "protocol.h"
#include "mcu.h"

struct mcu_port_config mcu_port[MCU_PORT_CNT];

// -----------------------------------------------------------------------
void mcu_disconnect()
{   
	DDRA = 0;
	PORTA = 0;
	DDRB = 0;
	PORTB = 0;
	DDRC = 0;
	PORTC = 0;
}	   

// -----------------------------------------------------------------------
void mcu_connect()
{
	DDRA = mcu_port[PA].output;
	DDRB = mcu_port[PB].output;
	DDRC = mcu_port[PC].output;
	PORTA = mcu_port[PA].pullup;
	PORTB = mcu_port[PB].pullup;
	PORTC = mcu_port[PC].pullup;
}

// -----------------------------------------------------------------------
void mcu_config_clear()
{
	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
		mcu_port[i].input = 0;
		mcu_port[i].output = 0;
		mcu_port[i].pullup = 0;
	}
}

// -----------------------------------------------------------------------
void mcu_pin_mask_clear()
{
	for (uint8_t i=0 ; i<MCU_PORT_CNT ; i++) {
		mcu_port[i].mask = 0;
	}
}

// -----------------------------------------------------------------------
void mcu_init()
{
	mcu_config_clear();
}

// -----------------------------------------------------------------------
bool mcu_func(uint8_t func, uint8_t port_pos, uint8_t port_bit)
{
	switch (func) {
		case ZIF_OUT:
			mcu_port[port_pos].output |= _BV(port_bit);
			break;
		case ZIF_IN:
			mcu_port[port_pos].input |= _BV(port_bit);
			break;
		case ZIF_IN_PU_WEAK:
			mcu_port[port_pos].input |= _BV(port_bit);
			mcu_port[port_pos].pullup |= _BV(port_bit);
			break;
		case ZIF_IN_PU_STRONG:
			mcu_port[port_pos].input |= _BV(port_bit);
			break;
		default:
			return false;
	}

	return true;
}

// -----------------------------------------------------------------------
void mcu_pin_unmasked(uint8_t port_pos, uint8_t port_bit)
{
	mcu_port[port_pos].mask |= mcu_port[port_pos].input & _BV(port_bit);
}

// -----------------------------------------------------------------------
struct mcu_port_config * mcu_get_port_config()
{
	return mcu_port;
}

// vim: tabstop=4 shiftwidth=4 autoindent
