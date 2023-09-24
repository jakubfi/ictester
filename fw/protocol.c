#include <inttypes.h>
#include <stdbool.h>

#include "protocol.h"
#include "serial.h"

static uint8_t error_reason = ERR_UNKNOWN;

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
uint8_t error(uint8_t reason)
{
	error_reason = reason;
	return RESP_ERR;
}

// -----------------------------------------------------------------------
uint8_t get_error()
{
	return error_reason;
}

// vim: tabstop=4 shiftwidth=4 autoindent
