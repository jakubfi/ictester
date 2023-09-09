#ifndef __LOGIC_H__
#define __LOGIC_H__

#include <inttypes.h>

uint8_t handle_vectors_load(uint8_t pin_count, uint8_t zif_vcc_pin);
uint8_t run_logic(uint8_t dut_pin_count, uint16_t loops, uint8_t *params);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
