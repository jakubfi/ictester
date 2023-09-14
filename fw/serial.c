//  Copyright (c) 2013 Jakub Filipowicz <jakubf@gmail.com>
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc.,
//  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

#include <stddef.h>
#include <inttypes.h>
#include <avr/io.h>

#include "serial.h"

// -----------------------------------------------------------------------
void serial_init(unsigned long baud)
{
	UCSR0A = 1 << U2X0;
	uint16_t speed = F_CPU / 8 / baud-1;
	UBRR0H = speed >> 8;
	UBRR0L = speed;
	UCSR0B = (1 << TXEN0) | (1 << RXEN0);
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); // 8N1
}

// -----------------------------------------------------------------------
void serial_tx_char(uint8_t c)
{
	while (!(UCSR0A & (1 << UDRE0)));
	UDR0 = c;
}

// -----------------------------------------------------------------------
uint8_t serial_rx_char()
{
	while (!(UCSR0A & (1 << RXC0)));
	return UDR0;
}

// -----------------------------------------------------------------------
uint16_t serial_rx_16le()
{
	uint16_t tmp = serial_rx_char();
	tmp |= (uint16_t) serial_rx_char() << 8;
	return tmp;
}

// -----------------------------------------------------------------------
void serial_tx_16le(uint16_t v)
{
	serial_tx_char(v & 0xff);
	serial_tx_char(v >> 8);
}

// -----------------------------------------------------------------------
void serial_tx_bytes(uint8_t *data, uint8_t count)
{
	while (count--) {
		serial_tx_char(*(data++));
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
