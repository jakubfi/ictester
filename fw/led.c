#include <inttypes.h>
#include <stdbool.h>
#include <util/delay.h>
#include <avr/io.h>

#include "external/pololu-led-strip-avr/led_strip.h"

#include "led.h"

// -----------------------------------------------------------------------
void led_init()
{
	LED_STRIP_PORT &= ~(1<<LED_STRIP_PIN);
	LED_STRIP_DDR |= (1<<LED_STRIP_PIN);
}

// -----------------------------------------------------------------------
void led(uint8_t r, uint8_t g, uint8_t b)
{
	rgb_color color = {r, g, b};
	led_strip_write(&color, 1);
}

// -----------------------------------------------------------------------
void led_welcome()
{
	for (int8_t i=30 ; i>=0 ; i--) {
		led(i, i, i);
		_delay_ms(6);
	}
	for (uint8_t i=30 ; i>=3 ; i--) {
		led(i, i, i);
		_delay_ms(5);
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
