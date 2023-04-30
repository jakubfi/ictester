#define F_CPU	16000000UL

#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "results.h"

//    pin:  7    6    5    4    3    2    1    0
// port A:  -   NC   Di  ~WE ~RAS   A0   A2   A1
// port C: NC   A7   A5   A4   A3   A6   Do ~CAS

#define PORT_RAS	PORTA
#define PORT_WE		PORTA
#define PORT_DIN	PORTA
#define PORT_CAS	PORTC
#define PIN_DOUT	PINC
#define PORT_AL		PORTA
#define PORT_AH		PORTC

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
#define READ_ONE  1
#define READ_NONE 2
#define WRITE_ZERO 0
#define WRITE_ONE  1
#define WRITE_NONE 2
#define DIR_UP 0
#define DIR_DOWN 1

register uint8_t addr_col asm("r2");
register uint8_t addr_row asm("r3");

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

typedef uint8_t (*march_fun)(uint8_t dir, uint8_t r, uint8_t w);


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
static inline uint8_t addr_low(uint8_t addr)
{
	return addr & 0b111;
}

// -----------------------------------------------------------------------
static inline uint8_t addr_high(uint8_t addr)
{
	return (addr & 0b11111000) >> 1;
}

// -----------------------------------------------------------------------
static inline void set_row_addr(uint8_t addr)
{
	PORT_AL = addr_low(addr) | VAL_WE | VAL_RAS;
	PORT_AH = addr_high(addr) | VAL_CAS;
	RAS_ON;
}

// -----------------------------------------------------------------------
static inline void set_col_addr(uint8_t addr)
{
	PORT_AL = addr_low(addr) | VAL_WE;
	PORT_AH = addr_high(addr) | VAL_CAS;
	CAS_ON;
}

// -----------------------------------------------------------------------
static inline uint8_t read_data(void)
{
	_NOP();
	_NOP();
	return (PIN_DOUT >> BIT_DO) & 1;
}

// -----------------------------------------------------------------------
static inline void write_data(uint8_t data)
{
	PORT_DIN = (PORT_DIN & ~(1<<BIT_DI)) | (data << BIT_DI);
	WE_ON;
	WE_OFF;
}

// -----------------------------------------------------------------------
// MARCH using read-write cycle (1.1s full pass)
// No need for additional refreshes, iterating over rows in the inner loop
// makes each row being refreshed every ~737ns
uint8_t march_step_rmw(uint8_t dir, uint8_t r, uint8_t w)
{
	uint8_t dout;

	do {
		if (dir == DIR_DOWN) addr_col--;
		do {
			if (dir == DIR_DOWN) addr_row--;
			set_row_addr(addr_row);
			set_col_addr(addr_col);
			// read always
			dout = read_data();
			if (w != WRITE_NONE) write_data(w);
			CAS_OFF;
			RAS_OFF;
			// check data only when required
			if ((r != READ_NONE) && (dout != r)) return RES_FAIL;
			if (dir == DIR_UP) addr_row++;
		} while (addr_row);
		if (dir == DIR_UP) addr_col++;
	} while (addr_col);

	return RES_PASS;
}

// -----------------------------------------------------------------------
// MARCH using read cycle + write cycle (1.5s full pass)
// No need for additional refreshes, as above.
uint8_t march_step_rw(uint8_t dir, uint8_t r, uint8_t w)
{
	uint8_t dout;

	do {
		if (dir == DIR_DOWN) addr_col--;
		do {
			if (dir == DIR_DOWN) addr_row--;

			// read always, check if required (faster than conditional read)
			set_row_addr(addr_row);
			set_col_addr(addr_col);
			dout = read_data();
			CAS_OFF;
			RAS_OFF;
			if ((r != READ_NONE) && (dout != r)) return RES_FAIL;

			if (w != WRITE_NONE) {
				set_row_addr(addr_row);
				set_col_addr(addr_col);
				write_data(w);
				CAS_OFF;
				RAS_OFF;
			}

			if (dir == DIR_UP) addr_row++;
		} while (addr_row);
		if (dir == DIR_UP) addr_col++;
	} while (addr_col);

	return RES_PASS;
}

// -----------------------------------------------------------------------
static inline void full_refresh(void)
{
	uint8_t addr_row_refresh = 0;
	do {
		set_row_addr(addr_row);
		RAS_OFF;
		addr_row_refresh++;
	} while (addr_row_refresh);
}

// -----------------------------------------------------------------------
// MARCH using full page reads and writes + refresh (1.2s full pass)
// It treats one page as a single "memory cell".
// This is for testing page access mode + refresh cycles
uint8_t march_step_page(uint8_t dir, uint8_t r, uint8_t w)
{
	uint8_t dout;

	if (r != READ_NONE) {
		do {
			if (dir == DIR_DOWN) addr_row--;
			set_row_addr(addr_row);

			do {
				if (dir == DIR_DOWN) addr_col--;
				set_col_addr(addr_col);
				dout = read_data();
				CAS_OFF;
				if (dout != r) return RES_FAIL;
				if (dir == DIR_UP) addr_col++;
			} while (addr_col);

			RAS_OFF;
			if (dir == DIR_UP) addr_row++;
			// do a full refresh every 4 rows == every ~1.9ms
			if ((addr_row & 0b11) == 0) full_refresh();

		} while (addr_row);
	}

	if (w != WRITE_NONE) {
		do {
			if (dir == DIR_DOWN) addr_row--;
			set_row_addr(addr_row);

			do {
				if (dir == DIR_DOWN) addr_col--;
				set_col_addr(addr_col);
				write_data(w);
				CAS_OFF;
				if (dir == DIR_UP) addr_col++;
			} while (addr_col);

			RAS_OFF;
			if (dir == DIR_UP) addr_row++;
			// full refresh every 4 rows == every 1.9ms
			if ((addr_row & 0b11) == 0) full_refresh();

		} while (addr_row);
	}

	return RES_PASS;
}

// -----------------------------------------------------------------------
uint8_t run_mem(uint8_t test)
{
	march_fun m_fun;

	switch (test) {
		case MEM_TEST_MARCH_RMW:
			m_fun = march_step_rmw;
			break;
		case MEM_TEST_MARCH_RW:
			m_fun = march_step_rw;
			break;
		case MEM_TEST_MARCH_PAGE:
			m_fun = march_step_page;
			break;
		default:
			return RES_FAIL;
	}

	for (uint8_t i=0 ; i<MARCH_STEPS ; i++) {
		if (m_fun(march_cm[i].dir, march_cm[i].read, march_cm[i].write) != RES_PASS) return RES_FAIL;
	}

	return RES_PASS;
}

// vim: tabstop=4 shiftwidth=4 autoindent
