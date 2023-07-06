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
	RESP_HELLO	= 129,
	RESP_OK		= 130,
	RESP_PASS	= 131,
	RESP_FAIL	= 132,
	RESP_ERR	= 133,
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
	ERR_PIN_SETUP	= 8,
	ERR_TEST_TYPE	= 9,
	ERR_PARAMS		= 10,
	ERR_VECT_NUM	= 11,
};

enum test_type {
	TYPE_COMB	= 0,
	TYPE_SEQ	= 1,
	TYPE_MEM	= 2,
	TYPE_MAX	= TYPE_MEM,
};

enum pin_type {
	PIN_IN	= 1,
	PIN_OUT	= 2,
	PIN_OC	= 3,
	PIN_VCC	= 4,
	PIN_GND	= 5,
	PIN_NC	= 6,
};

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
