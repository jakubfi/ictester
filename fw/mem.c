#define F_CPU	16000000UL

#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "results.h"

//    pin:  7    6    5    4    3    2    1    0
// port A:  -   A8*  Di  ~WE ~RAS   A0   A2   A1
// port C: NC   A7   A5   A4   A3   A6   Do ~CAS
//
// *only for 41256

#define PORT_RAS	PORTA
#define PORT_WE		PORTA
#define PORT_DIN	PORTA
#define PORT_CAS	PORTC
#define PIN_DOUT	PINC
#define PORT_ADDR_L		PORTA
#define PORT_ADDR_H		PORTC

#define BIT_WE		4
#define BIT_RAS		3
#define BIT_CAS		0
#define BIT_DO		1
#define BIT_DI		5

#define VAL_WE		(1 << BIT_WE)
#define VAL_RAS		(1 << BIT_RAS)
#define VAL_CAS		(1 << BIT_CAS)
#define VAL_DO		(1 << BIT_DO)
#define VAL_DI		(1 << BIT_DI)

#define WE_OFF		PORT_WE |= VAL_WE
#define WE_ON		PORT_WE &= ~VAL_WE
#define RAS_OFF		PORT_RAS |= VAL_RAS
#define RAS_ON		PORT_RAS &= ~VAL_RAS
#define CAS_OFF		PORT_CAS |= VAL_CAS
#define CAS_ON		PORT_CAS &= ~VAL_CAS

#define READ_ZERO 0
#define READ_ONE  VAL_DO
#define READ_NONE 2
#define WRITE_ZERO 0
#define WRITE_ONE  VAL_DI
#define WRITE_NONE 2
#define DIR_UP 0
#define DIR_DOWN 1

enum mem_test_type {
	MEM_TEST_MARCH_RMW		= 0,
	MEM_TEST_MARCH_RW		= 1,
	MEM_TEST_MARCH_PAGE		= 2,
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

// -----------------------------------------------------------------------
void mem_setup(void)
{
	DDRA  = 0b11111111;
	PORTA = 0b00011000;

	DDRC  = 0b11111101;
	PORTC = 0b00000001;

	// wait 500us after power-up (100-120us typical, but some chips apparently require 500us)
	_delay_us(500);

	// blink RAS 8 times before using the chip
	for (uint8_t i=0 ; i<8 ; i++) {
		RAS_ON;
		RAS_ON; // repeated twice, because 120ns min. pulse length
		RAS_OFF;
	}
}

// -----------------------------------------------------------------------
static inline uint8_t addr_low(uint16_t addr)
{
	return (addr & 0b111) | ((addr & 0b100000000) >> 2);
}

// -----------------------------------------------------------------------
static inline uint8_t addr_high(uint16_t addr)
{
	return (addr & 0b11111000) >> 1;
}

// -----------------------------------------------------------------------
static inline void set_row_addr(uint16_t addr, uint8_t dir)
{
	if (dir == DIR_DOWN) addr = ~addr;
	PORT_ADDR_L = addr_low(addr) | VAL_WE | VAL_RAS;
	PORT_ADDR_H = addr_high(addr) | VAL_CAS;
	RAS_ON;
}

// -----------------------------------------------------------------------
static inline void set_col_addr(uint16_t addr, uint8_t dir)
{
	if (dir == DIR_DOWN) addr = ~addr;
	PORT_ADDR_L = addr_low(addr) | VAL_WE;
	PORT_ADDR_H = addr_high(addr) | VAL_CAS;
	CAS_ON;
}

// -----------------------------------------------------------------------
static inline uint8_t read_data(void)
{
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
			if ((r != READ_NONE) && (read_data() != r)) return RESP_FAIL;
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
				if (read_data() != r) return RESP_FAIL;
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
				if (read_data() != r) return RESP_FAIL;
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
uint8_t run_mem(uint8_t *params)
{
	march_fun m_funcs[4] = {
		march_step_rmw,
		march_step_rw,
		march_step_page,
		march_step_page,
	};

	march_fun m_fun = m_funcs[params[1] & 0b11];
	uint16_t address_space = params[0] == 2 ? 0x200 : 0x100;

	for (uint8_t i=0 ; i<MARCH_STEPS ; i++) {
		if (m_fun(march_cm[i].dir, march_cm[i].read, march_cm[i].write, address_space) != RESP_PASS) {
			CAS_OFF;
			RAS_OFF;
			return RESP_FAIL;
		}
	}

	return RESP_PASS;
}

// vim: tabstop=4 shiftwidth=4 autoindent
