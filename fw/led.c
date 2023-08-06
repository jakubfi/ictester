#include <inttypes.h>
#include <stdbool.h>
#include <util/delay.h>
#include <avr/io.h>

#include "external/pololu-led-strip-avr/led_strip.h"

#include "led.h"

// -----------------------------------------------------------------------
void led_init(void)
{
	LED_STRIP_PORT &= ~(1<<LED_STRIP_PIN);
	LED_STRIP_DDR |= (1<<LED_STRIP_PIN);
}

// -----------------------------------------------------------------------
void led_welcome(void)
{
	rgb_color color;
	for (int8_t i=30 ; i>=0 ; i--) {
		color.red = i;
		color.green = i;
		color.blue = i;
		led_strip_write(&color, 1);
		_delay_ms(6);
	}
	for (uint8_t i=30 ; i>=3 ; i--) {
		color.red = i;
		color.green = i;
		color.blue = i;
		led_strip_write(&color, 1);
		_delay_ms(5);
	}
}

// -----------------------------------------------------------------------
void led_ok(void)
{
	rgb_color color;
	color.red = 0;
	color.green = 5;
	color.blue = 0;
	led_strip_write(&color, 1);
}

// -----------------------------------------------------------------------
void led_fail(void)
{
	rgb_color color;
	color.red = 5;
	color.green = 0;
	color.blue = 0;
	led_strip_write(&color, 1);
}

// -----------------------------------------------------------------------
void led_active(void)
{
	rgb_color color;
	color.red = 5;
	color.green = 2;
	color.blue = 0;
	led_strip_write(&color, 1);
}

// -----------------------------------------------------------------------
void led_comm(void)
{
	rgb_color color;
	color.red = 4;
	color.green = 0;
	color.blue = 3;
	led_strip_write(&color, 1);
}

// vim: tabstop=4 shiftwidth=4 autoindent
