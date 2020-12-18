#include <avr/io.h>
#include <inttypes.h>

void serial_init(unsigned long baud);
void serial_tx_char(uint8_t c);
void serial_tx_string(char *data);
uint8_t serial_rx_char(void);
unsigned char serial_rx_string(char *buf, unsigned char buf_size, char terminator);

