#include <util/delay.h>
#include <avr/io.h>

// -----------------------------------------------------------------------
void power_init()
{
	DDRD |= _BV(7); // output controlling the main power switch
}

// -----------------------------------------------------------------------
void power_on()
{
	PORTD |= _BV(7);
	// TPS2553 has a soft-start feature, needs ~3ms after powering on
	_delay_ms(3);
}

// -----------------------------------------------------------------------
void power_off()
{
	PORTD &= ~_BV(7);
	_delay_ms(3);
}

// vim: tabstop=4 shiftwidth=4 autoindent
