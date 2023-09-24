#ifndef __LOGIC_H__
#define __LOGIC_H__

#include <inttypes.h>

uint8_t handle_vectors_load(struct vectors *data, uint8_t pin_count, uint8_t zif_vcc_pin);
uint8_t logic_test_setup(uint8_t dut_pin_count, struct logic_params *params);
uint8_t run_logic(uint8_t dut_pin_count, uint16_t loops);
uint16_t logic_store_result(uint8_t *buf, uint8_t dut_pin_count);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
