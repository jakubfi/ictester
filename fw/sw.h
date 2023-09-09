#ifndef __SW_H__
#define __SW_H__

#include <inttypes.h>

#define A0 0 // analog switch 0, I2C bus A (top left)
#define A1 1 // analog switch 1, I2C bus A
#define A2 2 // analog switch 2, I2C bus A
#define B0 3 // analog switch 0, I2C bus B (top right)
#define B1 4 // analog switch 1, I2C bus B
#define NA -1 // not connected

#define SW_CFG_ALL 0
#define SW_CFG_GND_ONLY 1

void sw_init(void);
void sw_on(uint8_t port, uint8_t bit);
bool sw_config_sane(void);
void sw_push_config(uint8_t cfg);
void sw_connect(void);
void sw_disconnect(void);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
