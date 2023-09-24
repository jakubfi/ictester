#ifndef __DRAM_H__
#define __DRAM_H__

#include <inttypes.h>

void dram_connect();
uint8_t dram_test_setup(struct dram_params *params);
uint8_t dram_run(uint16_t loops);
uint16_t dram_store_result(uint8_t *buf, uint8_t dut_pin_count);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
