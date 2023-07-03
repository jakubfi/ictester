#define F_CPU	16000000UL

#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "results.h"
#include "serial.h"
#include "mem.h"

#define MAX_TEST_SIZE 1024

enum cmd {
	CMD_HELLO			= 1,
	CMD_DUT_SETUP		= 2,
	CMD_TEST_SETUP		= 3,
	CMD_VECTORS_LOAD	= 4,
	CMD_TEST_RUN		= 5,
	CMD_DUT_CONNECT		= 6,
	CMD_DUT_DISCONNECT	= 7,
};

enum test_type {
	TYPE_COMB	= 0,
	TYPE_SEQ	= 1,
	TYPE_MEM	= 2,
	TYPE_MAX	= TYPE_MEM,
};

enum pin_type {
	PIN_IN	= 1,
	PIN_OUT	= 2,
	PIN_OC	= 3,
	PIN_VCC	= 4,
	PIN_GND	= 5,
	PIN_NC	= 6,
};

struct port {
	uint8_t dut_input;
	uint8_t dut_output;
	uint8_t dut_pullup;
	uint8_t test_pin_mask;
} port[3];

uint8_t package_type;
uint8_t pin_count;
uint8_t dut_pin_bytes;
uint8_t test_type;
uint8_t test_subtype;
uint16_t test_len;
uint8_t test[MAX_TEST_SIZE][3];

struct pin_coord {
	int8_t port;
	int8_t pin;
} pin_coord;

const struct pin_coord *pin_map;

const struct pin_coord dip14_to_zif[14] = {
	{0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {-1, -1},
	{2, 0}, {2, 1}, {2, 2}, {2, 3}, {2, 4}, {2, 5}, {-1, -1}
};

const struct pin_coord dip14vcc5_to_zif[14] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1},
	{0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}, {0, 6}
};

const struct pin_coord dip14vcc4_to_zif[14] = {
	{2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1}, {2, 0},
	{0, 0}, {0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}
};

const struct pin_coord dip16_to_zif[16] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {2, 2}, {2, 1}, {2, 0}, {-1, -1},
	{0, 6}, {0, 5}, {0, 4}, {0, 3}, {0, 2}, {0, 1}, {0, 0}, {-1, -1}
};

const struct pin_coord dip16vcc8_to_zif[16] = {
	{0, 6}, {0, 5}, {0, 4}, {0, 3}, {0, 2}, {0, 1}, {0, 0}, {-1, -1},
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {2, 2}, {2, 1}, {2, 0}, {-1, -1}
};

const struct pin_coord dip16vcc5_to_zif[16] = {
	{2, 6}, {2, 5}, {2, 4}, {2, 3}, {-1, -1}, {2, 2}, {2, 1}, {2, 0},
	{0, 0}, {0, 1}, {0, 2}, {-1, -1}, {0, 3}, {0, 4}, {0, 5}, {0, 6}
};

const struct pin_coord dip24_to_zif[24] = {
	{0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {1, 0}, {1, 1}, {1, 2}, {-1, -1},
	{2, 0}, {2, 1}, {2, 2}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {1, 5}, {1, 4}, {1, 3}, {-1, -1}
};

// -----------------------------------------------------------------------
void reply(uint8_t res)
{
	serial_tx_char(res);
}

// -----------------------------------------------------------------------
void deconfigure(void)
{
	DDRA = 0;
	DDRB = 0;
	DDRC = 0;
	PORTA = 0;
	PORTB = 0;
	PORTC = 0;
}

// -----------------------------------------------------------------------
void setup(void)
{
	DDRA = port[0].dut_input;
	DDRB = port[1].dut_input;
	DDRC = port[2].dut_input;
}

// -----------------------------------------------------------------------
void handle_dut_setup(void)
{
	uint8_t pin_data[24];

	pin_map = NULL;

	// receive DUT configuration
	package_type = serial_rx_char();
	pin_count = serial_rx_char();
	dut_pin_bytes = (pin_count+7) / 8;
	for (uint8_t i=0 ; i<pin_count ; i++) {
		pin_data[i] = serial_rx_char();
	}

	// guess which socket to use
	if ((pin_count == 14) && (pin_data[6] == PIN_GND) && (pin_data[13] == PIN_VCC)) {
		pin_map = dip14_to_zif;
	} else if ((pin_count == 14) && (pin_data[9] == PIN_GND) && (pin_data[4] == PIN_VCC)) {
		pin_map = dip14vcc5_to_zif;
	} else if ((pin_count == 14) && (pin_data[10] == PIN_GND) && (pin_data[3] == PIN_VCC)) {
		pin_map = dip14vcc4_to_zif;
	} else if ((pin_count == 16) && (pin_data[7] == PIN_GND) && (pin_data[15] == PIN_VCC)) {
		pin_map = dip16_to_zif;
	} else if ((pin_count == 16) && (pin_data[7] == PIN_VCC) && (pin_data[15] == PIN_GND)) {
		pin_map = dip16vcc8_to_zif;
	} else if ((pin_count == 16) && (pin_data[11] == PIN_GND) && (pin_data[4] == PIN_VCC)) {
		pin_map = dip16vcc5_to_zif;
	} else if ((pin_count == 24) && (pin_data[11] == PIN_GND) && (pin_data[23] == PIN_VCC)) {
		pin_map = dip24_to_zif;
	}

	// no match for pin count/VCC/GND -> error
	if (!pin_map) {
		reply(RESP_ERR);
		return;
	}

	// clear current DUT configuration
	for (uint8_t i=0 ; i<3 ; i++) {
		port[i].dut_output = 0;
		port[i].dut_input = 0;
		port[i].dut_pullup = 0;
	}

	// prepare port configuration based on provided DUT pin config
	for (uint8_t i=0 ; i<pin_count ; i++) {
		// nothing to do for non-I/O pins
		if (pin_data[i] > PIN_OC) continue;

		int8_t port_pos = pin_map[i].port; // port this pin is connected to
		if (port_pos < 0) {
			// I/O pin is not connected to MCU. Shouldn't happen -> error
			reply(RESP_ERR);
			return;
		}
		uint8_t port_val = 1 << pin_map[i].pin;
		switch (pin_data[i]) {
			case PIN_IN:
				port[port_pos].dut_input |= port_val;
				break;
			case PIN_OUT:
				port[port_pos].dut_output |= port_val;
				break;
			case PIN_OC:
				port[port_pos].dut_pullup |= port_val;
				break;
			default:
				break;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
void handle_test_setup(void)
{
	test_type = serial_rx_char();
	test_subtype = serial_rx_char();

	// reset port masks
	port[0].test_pin_mask = 0;
	port[1].test_pin_mask = 0;
	port[2].test_pin_mask = 0;

	// read pin usage data
	uint8_t pin_usage[3];
	for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
		pin_usage[i] = serial_rx_char();
	}

	// fill in port masks
	for (uint8_t i=0 ; i<pin_count ; i++) {
		int8_t port_pos = pin_map[i].port;
		if (port_pos >= 0) {
			uint8_t pin_used = (pin_usage[i/8] >> (i%8)) & 1;
			uint8_t port_val = pin_used << pin_map[i].pin;
			port[port_pos].test_pin_mask |= port[port_pos].dut_output & port_val;
		}
	}

	reply(RESP_OK);
}

// -----------------------------------------------------------------------
void handle_vectors_load(void)
{
	test_len = serial_rx_16le();

	// receive all vectors
	for (uint16_t pos=0 ; pos<test_len ; pos++) {
		for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
			test[pos][i] = serial_rx_char();
		}
	}

	// reorder bits in each vector to match port connections
	for (uint16_t pos=0 ; pos<test_len ; pos++) {
		// convert received bytes into temporary 32-bit number
		uint32_t bitvector = 0;
		for (uint8_t i=0 ; i<dut_pin_bytes ; i++) {
			bitvector |= (uint32_t)test[pos][i] << (i*8);
		}
		// clear received vector data
		for (uint8_t i=0 ; i<3 ; i++) {
			test[pos][i] = 0;
		}
		// fill in bits in correct positions
		for (uint8_t pin=0 ; pin<pin_count ; pin++) {
			int8_t port_pos = pin_map[pin].port;
			if (port_pos >= 0) {
				uint8_t bit_val = (bitvector >> pin) & 1;
				test[pos][port_pos] |= bit_val << pin_map[pin].pin;
			}
		}
	}
	reply(RESP_OK);
}

// -----------------------------------------------------------------------
static inline void logic_port_setup(uint16_t pos)
{
	PORTA = ((test[pos][0] & port[0].dut_input) | port[0].dut_pullup);
	PORTB = ((test[pos][1] & port[1].dut_input) | port[1].dut_pullup);
	PORTC = ((test[pos][2] & port[2].dut_input) | port[2].dut_pullup);
}

// -----------------------------------------------------------------------
static inline bool logic_port_check(uint16_t pos)
{
	if ((test_type == TYPE_COMB) || (pos % 2)) {
		if ((PINA ^ test[pos][0]) & port[0].test_pin_mask) return false;
		if ((PINB ^ test[pos][1]) & port[1].test_pin_mask) return false;
		if ((PINC ^ test[pos][2]) & port[2].test_pin_mask) return false;
	}

	return true;
}

// -----------------------------------------------------------------------
uint8_t run_logic(void)
{
	// Seems that due to weak pull-ups in atmega, OC outputs take much longer to set up
	// Treat them separately to not slow down the test loop
	// ICs sensitive to that are: 7447, 74H62, 7489, 74156, 74170, 780101
	if (port[0].dut_pullup | port[1].dut_pullup | port[2].dut_pullup) {
		for (uint16_t pos=0 ; pos<test_len ; pos++) {
			logic_port_setup(pos);
			_NOP(); _NOP(); _NOP(); _NOP(); _NOP();
			_NOP(); _NOP(); _NOP(); _NOP(); _NOP();
			if (!logic_port_check(pos)) return RESP_FAIL;
		}
	} else {
		// ~3.9us per test cycle
		for (uint16_t pos=0 ; pos<test_len ; pos++) {
			logic_port_setup(pos);
			if (!logic_port_check(pos)) return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
void run(void)
{
	uint8_t res = RESP_PASS;

	uint8_t test_pow = serial_rx_char();
	int test_loops = pow(2, test_pow);

	if (test_type == TYPE_MEM) {
		mem_setup();
	} else {
		setup();
	}

	for (int rep=0 ; rep<test_loops ; rep++) {
		if (test_type == TYPE_MEM) {
			res = run_mem(test_subtype);
		} else {
			res = run_logic();
		}
		if (res != RESP_PASS) break;
	}

	deconfigure();

	reply(res);
}

// -----------------------------------------------------------------------
int main(void)
{
	deconfigure();
	serial_init(500000);

	while (1) {
		int cmd = serial_rx_char();
		switch (cmd) {
			case CMD_DUT_SETUP:
				handle_dut_setup();
				break;
			case CMD_TEST_SETUP:
				handle_test_setup();
				break;
			case CMD_VECTORS_LOAD:
				handle_vectors_load();
				break;
			case CMD_TEST_RUN:
				run();
				break;
			default:
				reply(RESP_ERR);
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
