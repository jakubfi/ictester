#ifndef __MCU_H__
#define __MCU_H__

#include <inttypes.h>

#define PA 0 // MCU port A
#define PB 1 // MCU port B
#define PC 2 // MCU port C

#define MCU_PORT_CNT 3

struct mcu_port_config {
	uint8_t output;
	uint8_t input;
	uint8_t pullup;
	uint8_t mask;
};

void mcu_init();
void mcu_config_select(uint8_t cfgnum);
void mcu_disconnect();
bool mcu_connect();
void mcu_config_clear();
bool mcu_func(uint8_t func, uint8_t port_pos, uint8_t port_bit);
struct mcu_port_config * mcu_get_port_config();

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
