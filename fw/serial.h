#ifndef __SERIAL_H__
#define __SERIAL_H__

#include <inttypes.h>

void serial_init(unsigned long baud);
void serial_tx_char(uint8_t c);
void serial_tx_bytes(uint8_t *data, uint8_t count);
uint8_t serial_rx_char();
uint16_t serial_rx_16le();
void serial_tx_16le(uint16_t v);
void serial_rx_bytes(uint8_t *data, uint16_t count);
#endif

// vim: tabstop=4 shiftwidth=4 autoindent
