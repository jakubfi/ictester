#ifndef __LED_H__
#define __LED_H__

#include <inttypes.h>

void led(uint8_t r, uint8_t g, uint8_t b);
void led_init();
void led_welcome();

#define LED_PASS	0, 5, 0
#define LED_FAIL	5, 0, 0
#define LED_ERR		4, 0, 3
#define LED_ACTIVE	5, 2, 0
#define LED_IDLE	3, 3, 3
#define LED_DEBUG	0, 0, 10

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
