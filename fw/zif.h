#ifndef __ZIF_H__
#define __ZIF_H__

#include <inttypes.h>
#include <stdbool.h>

void zif_init(void);
uint8_t zif_pos(uint8_t dut_pin_count, uint8_t dut_pin);
bool zif_func(uint8_t func, uint8_t pin);
bool zif_config_sane(void);
void zif_connect(void);
void zif_disconnect(void);

uint8_t mcu_port(uint8_t dut_pin);
uint8_t mcu_port_pin(uint8_t dut_pin);

#endif
