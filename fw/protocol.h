#ifndef __PROTOCOL_H__
#define __PROTOCOL_H__

#define MAX_TEST_PARAMS 4

enum commands {
	CMD_HELLO			= 1,
	CMD_DUT_SETUP		= 2,
	CMD_TEST_SETUP		= 3,
	CMD_VECTORS_LOAD	= 4,
	CMD_TEST_RUN		= 5,
	CMD_DUT_CONNECT		= 6,
	CMD_DUT_DISCONNECT	= 7,
};

enum responses {
	RESP_HELLO	= 128,
	RESP_OK		= 129,
	RESP_PASS	= 130,
	RESP_FAIL	= 131,
	RESP_ERR	= 132,
};

enum error_types {
	ERR_UNKNOWN		= 0,
	ERR_CMD			= 1,
	ERR_NO_SETUP	= 2,
	ERR_NO_TEST		= 3,
	ERR_NO_VECT		= 4,
	ERR_PACKAGE		= 5,
	ERR_PIN_CNT		= 6,
	ERR_PIN_FUNC	= 7,
	ERR_PIN_COMB	= 8,
	ERR_PIN_SETUP	= 9,
	ERR_TEST_TYPE	= 10,
	ERR_PARAMS		= 11,
	ERR_VECT_NUM	= 12,
};

enum test_type {
	TYPE_COMB	= 0,
	TYPE_SEQ	= 1,
	TYPE_MEM	= 2,
	TYPE_MAX	= TYPE_MEM,
};

enum package_type {
	PACKAGE_DIP = 1,
};

enum pin_type {
	PIN_IN	= 1,
	PIN_OUT	= 2,
	PIN_OC	= 3,
	PIN_3ST	= 4,
	PIN_OE = 5,
	PIN_C = 6,
	PIN_RC = 7,
	PIN_VCC	= 128,
	PIN_GND	= 129,
	PIN_NC	= 255,
};

void reply(uint8_t res);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
