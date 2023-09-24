#include <inttypes.h>
#include <stdbool.h>

#include "serial.h"

// -----------------------------------------------------------------------
bool receive_cmd(uint8_t *buf, uint16_t buf_size)
{
	uint16_t size = serial_rx_16le();

	if (size > buf_size) {
		// flush incomming data
		while (size--) serial_rx_char();
		return false;
	} else {
		serial_rx_bytes(buf, size);
		return true;
	}
}

// -----------------------------------------------------------------------
void send_response(uint8_t *buf, uint16_t len)
{
	serial_tx_16le(len);
	serial_tx_bytes(buf, len);
}

// -----------------------------------------------------------------------
void reply(uint8_t resp) 
{
	serial_tx_char(resp);
	// TODO: error codes
}

// vim: tabstop=4 shiftwidth=4 autoindent
