#ifndef __MEM_H__
#define __MEM_H__

#include <inttypes.h>

void mem_init();
uint8_t mem_test_setup(struct mem_params *params);
uint8_t run_mem(uint16_t loops);
uint16_t mem_store_result(uint8_t *buf, uint8_t dut_pin_count);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
