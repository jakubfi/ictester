#ifndef __LED_H__
#define __LED_H__

#include <inttypes.h>

#define LED_STRIP_PORT PORTA
#define LED_STRIP_DDR  DDRA
#define LED_STRIP_PIN  0

void led_init(void);
void led_welcome(void);
void led_pass(void);
void led_fail(void);
void led_err(void);
void led_idle(void);
void led_active(void);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
