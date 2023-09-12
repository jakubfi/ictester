#ifndef __PROTOCOL_H__
#define __PROTOCOL_H__

#define MAX_TEST_PARAMS 4
#define MAX_CONFIGS 4

enum commands {
	CMD_NONE			= 0,
	CMD_HELLO			= 1,
	CMD_DUT_SETUP		= 2,
	CMD_DUT_CONNECT		= 3,
	CMD_TEST_SETUP		= 4,
	CMD_VECTORS_LOAD	= 5,
	CMD_TEST_RUN		= 6,
	CMD_DUT_DISCONNECT	= 7,
};

enum responses {
	RESP_NONE	= 0,
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
	TEST_LOGIC	= 1,
	TEST_DRAM	= 2,
	TEST_UNIVIB	= 3,
	TEST_MAX	= TEST_UNIVIB
};

enum package_type {
	PACKAGE_DIP = 1,
};

enum zif_pin_function {
	ZIF_OUT				= 1,
	ZIF_IN				= 2,
	ZIF_IN_PU_STRONG	= 3,
	ZIF_IN_PU_WEAK		= 4,
	ZIF_OUT_SINK		= 5,
	ZIF_C				= 6,
	ZIF_OUT_SOURCE		= 7,
	ZIF_VCC				= 128,
	ZIF_GND				= 129,
	ZIF_IN_HIZ			= 255
};

void reply(uint8_t res);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
