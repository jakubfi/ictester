#ifndef __ZIF_H__
#define __ZIF_H__

#include <inttypes.h>

void zif_init();
uint8_t zif_pos(uint8_t dut_pin_count, uint8_t dut_pin);
bool zif_func(uint8_t cfgnum, uint8_t func, uint8_t zif_pin);
bool zif_connect(uint8_t cfgnum);
void zif_disconnect();
void zif_config_clear();
void zif_pin_mask_clear(uint8_t cfgnum);
void zif_pin_unmasked(uint8_t cfgnum, uint8_t zif_pin);
uint8_t zif_get_vcc_pin();

uint8_t zif_mcu_port(uint8_t zif_pin);
uint8_t zif_mcu_port_bit(uint8_t zif_pin);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
