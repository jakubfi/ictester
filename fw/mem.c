#define F_CPU	16000000UL

#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "results.h"

enum mem_test_type {
	MEM_TEST_BIT_ALL_0			= 0,
	MEM_TEST_BIT_ALL_1			= 1,
	MEM_TEST_ROW_ALL_0			= 2,
	MEM_TEST_ROW_ALL_1			= 3,
	MEM_TEST_ROW_ALTERNATE_01	= 4,
	MEM_TEST_ROW_ALTERNATE_10	= 5,
};

//    pin:  7   6   5   4    3  2  1    0
// port A:  -  NC Din ~WE ~RAS A0 A2   A1
// port C: NC  a7  a5  a4   a3 a6 Do ~CAS 

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
#define DATA		(PIN_DOUT >> 1) & 1;

#define ADDR_LOW(addr)	(((addr) & 0b111))
#define ADDR_HIGH(addr)	(((addr) & 0b11111000) >> 1)

#define SET_ROW_ADDR(addr)							\
	PORT_AL = ADDR_LOW(addr) | VAL_WE | VAL_RAS;	\
	PORT_AH = ADDR_HIGH(addr) | VAL_CAS;			\
	RAS_ON;

#define SET_COL_ADDR(addr)					\
	PORT_AL |= ADDR_LOW(addr);				\
	PORT_AH = ADDR_HIGH(addr) | VAL_CAS;	\
	CAS_ON;

// -----------------------------------------------------------------------
void mem_setup(void)
{
	DDRA  = 0b11111111;
	PORTA = 0b00011000;

	DDRC  = 0b11111101;
	PORTC = 0b00000001;

	// wait 500us after power-upn (120us typical, but some chips apparently require 500us)
	_delay_us(500);
	// blink RAS 8 times before using the chip
	for (uint8_t i=0 ; i<8 ; i++) {
		RAS_ON;
		RAS_ON; // repeated twice, because 120ns min pulse
		RAS_OFF;
	}
}

// -----------------------------------------------------------------------
uint8_t mem_test_bit(uint16_t addr, uint8_t data)
{
	uint8_t addr_col = addr & 0xff;
	uint8_t addr_row = addr >> 8;
	uint8_t dout;

	// --- WRITE ---

	SET_ROW_ADDR(addr_row);
	// early data
	WE_ON;
	PORT_DIN = (data & 1) << 5;
	SET_COL_ADDR(addr_col);
	// close
	WE_OFF;
	CAS_OFF;
	RAS_OFF;

	// --- READ ---

	SET_ROW_ADDR(addr_row);
	PORT_AL = VAL_WE;
	SET_COL_ADDR(addr_col);
	// wait for data and read
	_NOP();
	_NOP();
	dout = DATA;
	// close
	CAS_OFF;
	RAS_OFF;

	if (dout != data) return RES_FAIL;

	return RES_PASS;
}

// -----------------------------------------------------------------------
uint8_t mem_test_page(uint16_t addr, uint8_t data, uint8_t alternate)
{
	uint8_t res = RES_PASS;
	uint16_t addr_col;
	uint8_t addr_row = addr;
	uint8_t dout;

	// --- WRITE ---

	SET_ROW_ADDR(addr_row);
	for (addr_col=0 ; addr_col<256 ; addr_col++) {
		// data
		WE_ON;
		PORT_DIN = (data & 1) << 5;
		SET_COL_ADDR(addr_col);
		// close column
		WE_OFF;
		CAS_OFF;
		data ^= alternate;
	}
	// close row
	RAS_OFF;

	// --- READ ---

	SET_ROW_ADDR(addr_row);
	for (addr_col=0 ; addr_col<256 ; addr_col++) {
		PORT_AL = VAL_WE;
		SET_COL_ADDR(addr_col);
		// wait and read data
		_NOP();
		_NOP();
		dout = DATA;
		// close column
		CAS_OFF;
		// check data
		if (dout != data) {
			res = RES_FAIL;
			break;
		}
		data ^= alternate;
	}
	// close row
	RAS_OFF;

	return res;
}

// -----------------------------------------------------------------------
uint8_t run_mem(uint8_t test)
{
	uint8_t res = RES_PASS;
	uint32_t addr;
	uint8_t alternate = 0;
	uint8_t data = 0;

	if ((test == MEM_TEST_BIT_ALL_1) || (test == MEM_TEST_ROW_ALL_1) || (test == MEM_TEST_ROW_ALTERNATE_10)) {
		data = 1;
	}

	switch (test) {
		case MEM_TEST_BIT_ALL_0:
		case MEM_TEST_BIT_ALL_1:
			for (addr=0 ; addr<65536; addr++) {
				res = mem_test_bit(addr, data);
				if (res != RES_PASS) break;
			}
			break;
		case MEM_TEST_ROW_ALL_0:
		case MEM_TEST_ROW_ALL_1:
		case MEM_TEST_ROW_ALTERNATE_01:
		case MEM_TEST_ROW_ALTERNATE_10:
			if ((test == MEM_TEST_ROW_ALTERNATE_01) || (test == MEM_TEST_ROW_ALTERNATE_10)) {
				alternate = 1;
			}
			for (addr=0 ; addr<256; addr++) {
				res = mem_test_page(addr, data, alternate);
				if (res != RES_PASS) break;
			}
			break;
	}
	return res;
}

// vim: tabstop=4 shiftwidth=4 autoindent
