#define F_CPU	16000000UL

#include <math.h>
#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/cpufunc.h>
#include "serial.h"

#define MAX_TEST_SIZE 1024

enum cmd {
	CMD_SETUP	= 0,
	CMD_UPLOAD	= 1,
	CMD_RUN		= 2,
};

enum result {
	RES_OK		= 0,
	RES_ERR		= 1,
	RES_PASS	= 2,
	RES_FAIL	= 3,
};

enum type {
	TYPE_COMB	= 0,
	TYPE_SEQ	= 1,
	TYPE_MEM	= 2,
	TYPE_MAX	= TYPE_MEM,
};

struct port {
	volatile uint8_t *port;
	volatile uint8_t *pin;
	uint8_t dut_used;
	uint8_t dut_input;
	uint8_t dut_pullup;
} port[3];

uint8_t test_type;
uint8_t test_subtype;
uint16_t test_len;
uint8_t test[MAX_TEST_SIZE][3];

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
	DDRA = port[0].dut_input & port[0].dut_used;
	DDRB = port[1].dut_input & port[1].dut_used;
	DDRC = port[2].dut_input & port[2].dut_used;
}

// -----------------------------------------------------------------------
void read_setup(void)
{
	for (int i=0 ; i<3 ; i++) {
		port[i].dut_used = serial_rx_char();
		port[i].dut_input = serial_rx_char();
		port[i].dut_pullup = serial_rx_char();
	}

	reply(RES_OK);
}

// -----------------------------------------------------------------------
void upload(void)
{
	test_type = serial_rx_char();
	test_subtype = serial_rx_char();
	test_len = (uint16_t) serial_rx_char() << 8;
	test_len += serial_rx_char();

	for (int pos=0 ; pos<test_len ; pos++) {
		for (int i=0 ; i<3 ; i++) {
			test[pos][i] = serial_rx_char();
		}
	}

	reply(RES_OK);
}

// -----------------------------------------------------------------------
uint8_t run_logic(void)
{
	uint8_t i;
	uint8_t data;
	uint8_t pullup;
	uint8_t expected;

	uint8_t res = RES_PASS;
	for (int pos=0 ; pos<test_len ; pos++) {
		for (i=0 ; i<3 ; i++) {
			data = test[pos][i] & port[i].dut_input;
			pullup = port[i].dut_pullup & ~port[i].dut_input;
			*port[i].port = port[i].dut_used & (data | pullup);
		}
		_NOP();
		if ((test_type == TYPE_COMB) || ((test_type == TYPE_SEQ) && (pos%2))) {
			for (i=0 ; i<3 ; i++) {
				data = *port[i].pin & ~port[i].dut_input & port[i].dut_used;
				expected = test[pos][i] & ~port[i].dut_input & port[i].dut_used;
				if (data != expected) {
					res = RES_FAIL;
					break;
				}
			}
		}
	}
	return res;
}

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

	// wait 100us after initialization
	_delay_us(100);
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

#define MEM_TEST_BIT_ALL_0 0
#define MEM_TEST_BIT_ALL_1 1
#define MEM_TEST_ROW_ALL_0 2
#define MEM_TEST_ROW_ALL_1 3
#define MEM_TEST_ROW_ALTERNATE_01 4
#define MEM_TEST_ROW_ALTERNATE_10 5

// -----------------------------------------------------------------------
uint8_t run_mem(void)
{
	uint8_t res = RES_PASS;
	uint32_t addr;
	uint8_t alternate = 0;
	uint8_t data = 0;

	if ((test_subtype == MEM_TEST_BIT_ALL_1) || (test_subtype == MEM_TEST_ROW_ALL_1) || (test_subtype == MEM_TEST_ROW_ALTERNATE_10)) {
		data = 1;
	}

	switch (test_subtype) {
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
			if ((test_subtype == MEM_TEST_ROW_ALTERNATE_01) || (test_subtype == MEM_TEST_ROW_ALTERNATE_10)) {
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

// -----------------------------------------------------------------------
void run(void)
{
	uint8_t res = RES_PASS;

	uint8_t test_pow = serial_rx_char();
	int test_loops = pow(2, test_pow);

	if (test_type == TYPE_MEM) {
		mem_setup();
	} else {
		setup();
	}

	for (int rep=0 ; rep<test_loops ; rep++) {
		if (test_type == TYPE_MEM) {
			res = run_mem();
		} else {
			res = run_logic();
		}
		if (res != RES_PASS) break;
	}

	deconfigure();

	reply(res);
}

// -----------------------------------------------------------------------
int main(void)
{
	deconfigure();
	serial_init(500000);

	port[0].port = &PORTA;
	port[1].port = &PORTB;
	port[2].port = &PORTC;
	port[0].pin = &PINA;
	port[1].pin = &PINB;
	port[2].pin = &PINC;

	while (1) {
		int cmd = serial_rx_char();
		switch (cmd) {
			case CMD_SETUP:
				read_setup();
				break;
			case CMD_UPLOAD:
				upload();
				break;
			case CMD_RUN:
				run();
				break;
			default:
				reply(RES_ERR);
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
