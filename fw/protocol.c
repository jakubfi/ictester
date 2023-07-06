#include <inttypes.h>

#include "serial.h"

// -----------------------------------------------------------------------
void reply(uint8_t resp) 
{
	serial_tx_char(resp);
	// TODO: error codes
}

// vim: tabstop=4 shiftwidth=4 autoindent
