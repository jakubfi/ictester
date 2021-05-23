#define F_CPU	16000000UL

#include <inttypes.h>
#include <math.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "results.h"
#include "serial.h"
#include "mem.h"

enum cmd {
	CMD_SETUP	= 0,
	CMD_UPLOAD	= 1,
	CMD_RUN		= 2,
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
			res = run_mem(test_subtype);
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
