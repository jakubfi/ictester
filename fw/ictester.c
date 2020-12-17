#define F_CPU	16000000UL

#include <math.h>
#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/cpufunc.h>
#include "serial.h"

#define MAX_TEST_SIZE 3*1024

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
	TYPE_MAX	= TYPE_SEQ,
};

struct port_conf {
	uint8_t dut_inputs;
	uint8_t dut_used;
} port_conf[3];

uint8_t test_type;
uint16_t test_len;
uint8_t test_data[MAX_TEST_SIZE];

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
	DDRA = port_conf[0].dut_inputs & port_conf[0].dut_used;
	DDRB = port_conf[1].dut_inputs & port_conf[1].dut_used;
	DDRC = port_conf[2].dut_inputs & port_conf[2].dut_used;
}

// -----------------------------------------------------------------------
void read_setup(uint8_t cmd)
{
	for (int i=0 ; i<3 ; i++) {
		port_conf[i].dut_used = serial_rx_char();
		port_conf[i].dut_inputs = serial_rx_char();
	}

	reply(RES_OK);
}

// -----------------------------------------------------------------------
void upload(uint8_t cmd)
{
	test_type = serial_rx_char();
	test_len = (uint16_t) serial_rx_char() << 8;
	test_len += serial_rx_char();

	for (int pos=0 ; pos<test_len*3 ; pos++) {
		test_data[pos] = serial_rx_char();
	}

	reply(RES_OK);
}

// -----------------------------------------------------------------------
uint8_t run_single(void)
{
	uint8_t dA, dB, dC;

	uint8_t res = RES_PASS;
	for (int pos=0 ; pos<test_len ; pos++) {
		PORTA = test_data[pos*3+0] & port_conf[0].dut_inputs & port_conf[0].dut_used;
		PORTB = test_data[pos*3+1] & port_conf[1].dut_inputs & port_conf[1].dut_used;
		PORTC = test_data[pos*3+2] & port_conf[2].dut_inputs & port_conf[2].dut_used;
		_NOP();
		if ((test_type == TYPE_COMB) || ((test_type == TYPE_SEQ) && (pos%2))) {
			dA = PINA & ~port_conf[0].dut_inputs & port_conf[0].dut_used;
			dB = PINB & ~port_conf[1].dut_inputs & port_conf[1].dut_used;
			dC = PINC & ~port_conf[2].dut_inputs & port_conf[2].dut_used;
			if ((dA != (test_data[pos*3+0] & ~port_conf[0].dut_inputs & port_conf[0].dut_used))
			| (dB != (test_data[pos*3+1] & ~port_conf[1].dut_inputs & port_conf[1].dut_used))
			| (dC != (test_data[pos*3+2] & ~port_conf[2].dut_inputs & port_conf[2].dut_used))) {
				res = RES_FAIL;
				break;
			}
		}
	}
	return res;
}

// -----------------------------------------------------------------------
void run(uint8_t cmd)
{
	uint8_t res;

	uint8_t test_pow = serial_rx_char();
	int test_loops = pow(2, test_pow);

	for (int rep=0 ; rep<test_loops ; rep++) {
		res = run_single();
		if (res != RES_PASS) {
			reply(RES_FAIL);
			return;
		}
	}

	reply(RES_PASS);
}

// -----------------------------------------------------------------------
int main(void)
{
	deconfigure();
	serial_init();

	while (1) {
		int cmd = serial_rx_char();
		switch (cmd >> 5) {
			case CMD_SETUP:
				read_setup(cmd);
				break;
			case CMD_UPLOAD:
				upload(cmd);
				break;
			case CMD_RUN:
				setup();
				run(cmd);
				deconfigure();
				break;
			default:
				reply(RES_ERR);
		}
	}

	return 0;
}
