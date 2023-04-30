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

#define MAX_TEST_SIZE 1024

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
	for (uint16_t pos=0 ; pos<test_len ; pos++) {
		PORTA = port[0].dut_used & ((test[pos][0] & port[0].dut_input) | (port[0].dut_pullup & ~port[0].dut_input));
		PORTB = port[1].dut_used & ((test[pos][1] & port[1].dut_input) | (port[1].dut_pullup & ~port[1].dut_input));
		PORTC = port[2].dut_used & ((test[pos][2] & port[2].dut_input) | (port[2].dut_pullup & ~port[2].dut_input));

		if ((test_type == TYPE_COMB) || ((test_type == TYPE_SEQ) && (pos%2))) {
			if ((PINA & ~port[0].dut_input & port[0].dut_used) != (test[pos][0] & ~port[0].dut_input & port[0].dut_used)) return RES_FAIL;
			if ((PINB & ~port[1].dut_input & port[1].dut_used) != (test[pos][1] & ~port[1].dut_input & port[1].dut_used)) return RES_FAIL;
			if ((PINC & ~port[2].dut_input & port[2].dut_used) != (test[pos][2] & ~port[2].dut_input & port[2].dut_used)) return RES_FAIL;
		}
	}

	return RES_PASS;
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
