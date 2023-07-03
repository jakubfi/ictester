#include <avr/io.h>
#include <inttypes.h>

void serial_init(unsigned long baud);
void serial_tx_char(uint8_t c);
uint8_t serial_rx_char(void);
uint16_t serial_rx_16le(void);

