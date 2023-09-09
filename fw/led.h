#ifndef __LED_H__
#define __LED_H__

#include <inttypes.h>

#define LED_STRIP_PORT PORTA
#define LED_STRIP_DDR  DDRA
#define LED_STRIP_PIN  0

void led_init();
void led_welcome();
void led_pass();
void led_fail();
void led_err();
void led_idle();
void led_active();

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
