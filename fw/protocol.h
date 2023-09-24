#ifndef __PROTOCOL_H__
#define __PROTOCOL_H__

#define MAX_TEST_PARAMS 2
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
	RESP_NONE			= 0,
	RESP_HELLO			= 128,
	RESP_OK				= 129,
	RESP_PASS			= 130,
	RESP_FAIL			= 131,
	RESP_ERR			= 132,
	RESP_TIMING_ERROR	= 133,
};

enum error_types {
	ERR_UNKNOWN		= 0,	// unknown error (not set by the FW, likely a bug)
	ERR_CMD_UNKNOWN	= 1,	// unknown command
	ERR_CMD_TOOBIG	= 2,	// command didn't fit in the buffer
	ERR_CRC			= 3,	// CRC transmission error detected
	ERR_4			= 4,
	ERR_PACKAGE		= 5,	// unknown DUT package
	ERR_PIN_CNT		= 6,	// wrong DUT pin count
	ERR_PIN_FUNC	= 7,	// unknown DUT pin function
	ERR_PIN_COMB	= 8,	// wrong (unsafe) pin function combination
	ERR_9			= 9,
	ERR_TEST_TYPE	= 10,	// unknown test type
	ERR_11			= 11,
	ERR_VECT_NUM	= 12,	// too many vectors or no vectors at all
	ERR_PINCFG_CNT	= 13,	// wrong pin configuration count
	ERR_PINCFG_NUM	= 14,	// wrong pin configuration number (pin configuration not set)
	ERR_15			= 15,
	ERR_PIN_FUNC_UNAVAILABLE = 16,	// function not available for a pin
	ERR_NO_PINCFG	= 17,	// no pin configuration active
	ERR_UNKNOWN_CHIP	= 18,	// selected chip type is unknown
	ERR_UNKNOWN_TEST	= 19,	// no such test for selected chip
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
	ZIF_IN_HIZ			= 2,
	ZIF_IN_PU_STRONG	= 3,
	ZIF_IN_PU_WEAK		= 4,
	ZIF_OUT_SINK		= 5,
	ZIF_C				= 6,
	ZIF_OUT_SOURCE		= 7,
	ZIF_VCC				= 128,
	ZIF_GND				= 129,
};

struct cmd {
	uint8_t cmd;
	uint8_t data[];
};

struct cmd_dut_setup {
	uint8_t package;
	uint8_t pin_count;
	uint8_t cfg_count;
	uint8_t configs[];
};

struct cmd_test_setup {
	uint8_t cfg_num;
	uint8_t test_type;
	uint8_t params[];
};

struct cmd_dut_connect {
	uint8_t cfg_num;
};

struct cmd_run {
	uint16_t loops;
};

struct logic_params {
	uint16_t delay;
	uint8_t pin_usage[];
};

struct dram_params {
	uint8_t device;
	uint8_t test_type;
};

struct univib_params {
	uint8_t device;
	uint8_t test_type;
};

struct vectors {
	uint16_t vector_cnt;
	uint8_t vectors[];
};

struct resp_logic_fail {
	uint16_t vector_num;
	uint8_t vector[];
};

struct resp_dram_fail {
	uint16_t row_address;
	uint16_t column_address;
	uint8_t march_step;
};

bool receive_cmd(uint8_t *buf, uint16_t buf_size);
void send_response(uint8_t *buf, uint16_t len);
uint8_t error(uint8_t reason);
uint8_t get_error();

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
