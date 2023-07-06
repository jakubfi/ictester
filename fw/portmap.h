#ifndef __PORTMAP_H__
#define __PORTMAP_H__

#include <inttypes.h>
#include <stdbool.h>

bool guess_socket(uint8_t pin_count, uint8_t *pin_data);
uint8_t mcu_port(uint8_t dut_pin);
uint8_t mcu_port_pin(uint8_t dut_pin);

#endif
