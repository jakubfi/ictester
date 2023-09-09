#ifndef __SERIAL_H__
#define __SERIAL_H__

#include <inttypes.h>

void serial_init(unsigned long baud);
void serial_tx_char(uint8_t c);
uint8_t serial_rx_char();
uint16_t serial_rx_16le();

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
