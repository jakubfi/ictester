#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "protocol.h"

//    pin:  7    6    5    4    3    2    1    0
// port C:  -   A1   A2   A0 ~RAS  ~WE   Di   A8*
// port B:  - ~CAS   Do   A6   A3   A4   A5   A7
//
// *only for 41256

#define PORT_RAS	PORTC
#define PORT_WE		PORTC
#define PORT_DIN	PORTC
#define PORT_CAS	PORTB
#define PORT_DOUT	PORTB
#define PIN_DOUT	PINB
#define PORT_ADDR_L	PORTC
#define PORT_ADDR_H	PORTB

#define VAL_WE		_BV(2)
#define VAL_RAS		_BV(3)
#define VAL_CAS		_BV(6)
#define VAL_DO		_BV(5)
#define VAL_DI		_BV(1)

#define WE_OFF		PORT_WE |= VAL_WE
#define WE_ON		PORT_WE &= ~VAL_WE
#define RAS_OFF		PORT_RAS |= VAL_RAS
#define RAS_ON		PORT_RAS &= ~VAL_RAS
#define CAS_OFF		PORT_CAS |= VAL_CAS
#define CAS_ON		PORT_CAS &= ~VAL_CAS

#define DOUT_PULLUP	(PORT_DOUT & VAL_DO)

#define READ_ZERO 0
#define READ_ONE  VAL_DO
#define READ_NONE 255
#define WRITE_ZERO 0
#define WRITE_ONE  VAL_DI
#define WRITE_NONE 255
#define DIR_UP 0
#define DIR_DOWN 1

enum dram_chip_type {
	DRAM_4164		= 1,
	DRAM_41256		= 2,
	DRAM_DEVICE_MAX = DRAM_41256
};

enum dram_test_type {
	DRAM_TEST_SPEED			= 0,
	DRAM_TEST_MARCH_RMW		= 1,
	DRAM_TEST_MARCH_RW		= 2,
	DRAM_TEST_MARCH_PAGE	= 3,
	DRAM_TEST_MAX			= DRAM_TEST_MARCH_PAGE
};

struct march {
	uint8_t dir;
	uint8_t read;
	uint8_t write;
};

#define MARCH_STEPS 6
static const struct march march_cm[MARCH_STEPS] = {
	{ DIR_UP,   READ_NONE, WRITE_ZERO }, // any(w0)
	{ DIR_UP,   READ_ZERO, WRITE_ONE  }, // up(r0,w1)
	{ DIR_UP,   READ_ONE,  WRITE_ZERO }, // up(r1,w0)
	{ DIR_DOWN, READ_ZERO, WRITE_ONE  }, // down(r0,w1)
	{ DIR_DOWN, READ_ONE,  WRITE_ZERO }, // down(r1,w0)
	{ DIR_UP,   READ_ZERO, WRITE_NONE }, // up(r0)
};

typedef uint8_t (*march_fun)(uint8_t dir, uint8_t r, uint8_t w, uint16_t addr_space);

uint8_t dram_device;
uint8_t dram_test_type;

uint16_t failing_row, failing_col;
uint8_t failing_step;

// -----------------------------------------------------------------------
uint8_t dram_test_setup(struct dram_params *params)
{
	if (params->device > DRAM_DEVICE_MAX) {
		return error(ERR_UNKNOWN_CHIP);
	}
	if (params->test_type > DRAM_TEST_MAX) {
		return error(ERR_UNKNOWN_TEST);
	}

	dram_device = params->device;
	dram_test_type = params->test_type;

	return RESP_OK;
}

// -----------------------------------------------------------------------
void dram_connect()
{
	CAS_OFF;
	RAS_OFF;
	WE_OFF;

	// wait 500us after power-up (100-120us typical, but some chips apparently require 500us)
	_delay_us(500);

	// blink RAS 8 times before using the chip
	for (uint8_t i=0 ; i<8 ; i++) {
		RAS_ON;
		_NOP(); _NOP(); // 120ns min. pulse length
		RAS_OFF;
	}
}

// -----------------------------------------------------------------------
static inline uint8_t addr_low(uint16_t addr)
{
	return ((addr & 0b11100000) >> 1) | ((addr & 0b100000000) >> 8);
}

// -----------------------------------------------------------------------
static inline uint8_t addr_high(uint16_t addr)
{
	return addr & 0b11111;
}

// -----------------------------------------------------------------------
static inline void set_row_addr(uint16_t addr, uint8_t dir)
{
	if (dir == DIR_DOWN) addr = ~addr;
	PORT_ADDR_L = addr_low(addr) | VAL_WE | VAL_RAS;
	PORT_ADDR_H = DOUT_PULLUP | addr_high(addr) | VAL_CAS;
	RAS_ON;
}

// -----------------------------------------------------------------------
static inline void set_col_addr(uint16_t addr, uint8_t dir)
{
	if (dir == DIR_DOWN) addr = ~addr;
	PORT_ADDR_L = addr_low(addr) | VAL_WE;
	PORT_ADDR_H = DOUT_PULLUP | addr_high(addr) | VAL_CAS;
	CAS_ON;
}

// -----------------------------------------------------------------------
static inline uint8_t read_data(void)
{
	_NOP();
	_NOP();
	_NOP();
	return PIN_DOUT & VAL_DO;
}

// -----------------------------------------------------------------------
static inline void write_data(uint8_t data)
{
	PORT_DIN = (PORT_DIN & ~VAL_DI) | data;
	WE_ON;
	WE_OFF;
}

// -----------------------------------------------------------------------
// MARCH using read-write cycle
static uint8_t march_step_rmw(uint8_t dir, uint8_t r, uint8_t w, uint16_t addr_space)
{
	for (uint16_t addr_col=0 ; addr_col < addr_space; addr_col++) {
		for (uint16_t addr_row=0 ; addr_row < addr_space; addr_row++) {
			set_row_addr(addr_row, dir);
			set_col_addr(addr_col, dir);
			if ((r != READ_NONE) && (read_data() != r)) {
				failing_row = addr_row;
				failing_col = addr_col;
				return RESP_FAIL;
			}
			if (w != WRITE_NONE) write_data(w);
			CAS_OFF;
			RAS_OFF;
		}
	}
	return RESP_PASS;
}

// -----------------------------------------------------------------------
// MARCH using read cycle + write cycle
static uint8_t march_step_rw(uint8_t dir, uint8_t r, uint8_t w, uint16_t addr_space)
{
	for (uint16_t addr_col=0 ; addr_col < addr_space; addr_col++) {
		for (uint16_t addr_row=0 ; addr_row < addr_space; addr_row++) {
			if (r != READ_NONE) {
				set_row_addr(addr_row, dir);
				set_col_addr(addr_col, dir);
				if (read_data() != r) {
					failing_row = addr_row;
					failing_col = addr_col;
					return RESP_FAIL;
				}
				CAS_OFF;
				RAS_OFF;
			}

			if (w != WRITE_NONE) {
				set_row_addr(addr_row, dir);
				set_col_addr(addr_col, dir);
				write_data(w);
				CAS_OFF;
				RAS_OFF;
			}
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline void full_refresh(uint16_t addr_space)
{
	for (uint16_t addr=0 ; addr < addr_space ; addr++) {
		set_row_addr(addr, DIR_UP);
		RAS_OFF;
	}
}

// -----------------------------------------------------------------------
// MARCH using full page reads and writes + refresh (treats one page as a single "memory cell")
static uint8_t march_step_page(uint8_t dir, uint8_t r, uint8_t w, uint16_t addr_space)
{
	if (r != READ_NONE) {
		for (uint16_t addr_row=0 ; addr_row < addr_space; addr_row++) {
			set_row_addr(addr_row, dir);
			for (uint16_t addr_col=0 ; addr_col < addr_space; addr_col++) {
				set_col_addr(addr_col, dir);
				if (read_data() != r) {
					failing_row = addr_row;
					failing_col = addr_col;
					return RESP_FAIL;
				}
				CAS_OFF;
			}
			RAS_OFF;
			if ((addr_row & 0b11) == 0) full_refresh(addr_space);
		}
	}

	if (w != WRITE_NONE) {
		for (uint16_t addr_row=0 ; addr_row < addr_space; addr_row++) {
			set_row_addr(addr_row, dir);
			for (uint16_t addr_col=0 ; addr_col < addr_space; addr_col++) {
				set_col_addr(addr_col, dir);
				write_data(w);
				CAS_OFF;
			}
			RAS_OFF;
			if ((addr_row & 0b11) == 0) full_refresh(addr_space);
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
void test_speed(uint16_t loops)
{
	uint8_t w = 0;
	for (uint16_t addr_col=0 ; addr_col < 256 ; addr_col++) {
		for (uint16_t addr_row=0 ; addr_row < 256 ; addr_row++) {
			set_row_addr(addr_row, DIR_UP);
			set_col_addr(addr_col, DIR_UP);
			write_data(w);
			w ^= WRITE_ONE;
			CAS_OFF;
			RAS_OFF;
		}
	}

	for (uint16_t rep=0 ; rep<loops ; rep++) {
		for (uint16_t addr_col=0 ; addr_col < 256 ; addr_col++) {
			for (uint16_t addr_row=0 ; addr_row < 256 ; addr_row++) {
				set_row_addr(addr_row, DIR_UP);
				set_col_addr(addr_col, DIR_UP);
				read_data();
				CAS_OFF;
				RAS_OFF;
			}
		}
	}
}

// -----------------------------------------------------------------------
uint8_t dram_run(uint16_t loops)
{
	march_fun m_funcs[4] = {
		[DRAM_TEST_SPEED] = NULL,
		[DRAM_TEST_MARCH_RMW] = march_step_rmw,
		[DRAM_TEST_MARCH_RW] = march_step_rw,
		[DRAM_TEST_MARCH_PAGE] = march_step_page,
	};

	uint16_t address_space;
	switch (dram_device) {
		case DRAM_4164:
			address_space = 0x100;
			break;
		case DRAM_41256:
			address_space = 0x200;
			break;
		default:
			return error(ERR_UNKNOWN_CHIP);
	}

	if (dram_test_type == DRAM_TEST_SPEED) {
		test_speed(loops);
		return RESP_PASS;
	}

	if (dram_test_type > DRAM_TEST_MAX) {
		return error(ERR_UNKNOWN_TEST);
	}

	march_fun m_fun = m_funcs[dram_test_type];

	for (uint16_t rep=0 ; rep<loops ; rep++) {
		for (uint8_t i=0 ; i<MARCH_STEPS ; i++) {
			if (m_fun(march_cm[i].dir, march_cm[i].read, march_cm[i].write, address_space) != RESP_PASS) {
				failing_step = i;
				CAS_OFF;
				RAS_OFF;
				return RESP_FAIL;
			}
		}
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
uint16_t dram_store_result(uint8_t *buf, uint8_t dut_pin_count)
{
	struct resp_dram_fail *resp = (struct resp_dram_fail*) buf;
	resp->row_address = failing_row;
	resp->column_address = failing_col;
	resp->march_step = failing_step;
	return 5;
}

// vim: tabstop=4 shiftwidth=4 autoindent
