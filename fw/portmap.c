#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>

#include "protocol.h"

struct pin_coord {
	int8_t port;
	int8_t pin;
} pin_coord;

const __flash struct pin_coord dip14_to_zif[14] = {
	{0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {-1, -1},
	{2, 0}, {2, 1}, {2, 2}, {2, 3}, {2, 4}, {2, 5}, {-1, -1}
};

const __flash struct pin_coord dip14vcc5_to_zif[14] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1},
	{0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}, {0, 6}
};

const __flash struct pin_coord dip14vcc4_to_zif[14] = {
	{2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1}, {2, 0},
	{0, 0}, {0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}
};

const __flash struct pin_coord dip16_to_zif[16] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {2, 2}, {2, 1}, {2, 0}, {-1, -1},
	{0, 6}, {0, 5}, {0, 4}, {0, 3}, {0, 2}, {0, 1}, {0, 0}, {-1, -1}
};

const __flash struct pin_coord dip16vcc8_to_zif[16] = {
	{0, 6}, {0, 5}, {0, 4}, {0, 3}, {0, 2}, {0, 1}, {0, 0}, {-1, -1},
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {2, 2}, {2, 1}, {2, 0}, {-1, -1}
};

const __flash struct pin_coord dip16vcc5_to_zif[16] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1}, {2, 0},
	{0, 0}, {0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}, {0, 6}
};

const __flash struct pin_coord dip24_to_zif[24] = {
	{0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {1, 0}, {1, 1}, {1, 2}, {-1, -1},
	{2, 0}, {2, 1}, {2, 2}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {1, 5}, {1, 4}, {1, 3}, {-1, -1}
};

const __flash struct pin_coord *pin_map;

struct socket_properties {
	uint8_t pins, gnd, vcc;
	const __flash struct pin_coord *pin_map;
};

const __flash struct socket_properties sp[] = {
	{14, 6, 13, dip14_to_zif},
	{14, 9, 4, dip14vcc5_to_zif},
	{14, 10, 3, dip14vcc4_to_zif},
	{16, 7, 15, dip16_to_zif},
	{16, 15, 7, dip16vcc8_to_zif},
	{16, 11, 4, dip16vcc5_to_zif},
	{24, 11, 23, dip24_to_zif},
	{-1, -1, -1, NULL}
};

// -----------------------------------------------------------------------
bool guess_socket(uint8_t pin_count, uint8_t *pin_data)
{
	pin_map = NULL;

	// find which socket to use
	const __flash struct socket_properties *tab = sp;
	while (tab->pin_map) {
		if ((pin_count == tab->pins) && (pin_data[tab->gnd] == PIN_GND) && (pin_data[tab->vcc] == PIN_VCC)) {
			pin_map = tab->pin_map;
			break;
		}
		tab++;
	}

	return pin_map != NULL;
}

// -----------------------------------------------------------------------
uint8_t mcu_port(uint8_t dut_pin)
{
	return pin_map[dut_pin].port;
}

// -----------------------------------------------------------------------
uint8_t mcu_port_pin(uint8_t dut_pin)
{
	return pin_map[dut_pin].pin;
}

// vim: tabstop=4 shiftwidth=4 autoindent
