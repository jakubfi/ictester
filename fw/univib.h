#ifndef __UNIVIB_H__
#define __UNIVIB_H__

#include <inttypes.h>

uint8_t univib_test_setup(struct univib_params *params);
uint8_t run_univib(uint16_t loops);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
