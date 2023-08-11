#include <inttypes.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/cpufunc.h>
#include <util/delay.h>

#include "protocol.h"

#define PARAM_DEV 0
#define PARAM_TEST 1

#define UNIVIB_121 0
#define UNIVIB_122 1
#define UNIVIB_123_1 2
#define UNIVIB_123_2 3

#define TEST_NOTRIG 0
#define TEST_TRIG 1
#define TEST_RETRIG 2
#define TEST_CLEAR 3
#define TEST_CROSSTRIG 4

#define LAST_TRIG 0xff

// 74121

#define VAL_121_A1 _BV(2)
#define VAL_121_A2 _BV(3)
#define VAL_121_B _BV(4)
#define VAL_121_Q _BV(5)
#define VAL_121_NQ _BV(0)

// 74122

#define VAL_122_A1 _BV(0)
#define VAL_122_A2 _BV(1)
#define VAL_122_B1 _BV(2)
#define VAL_122_B2 _BV(3)
#define VAL_122_CLR _BV(4)
#define VAL_122_NQ _BV(5)
#define VAL_122_Q _BV(1)

// 74123 1 and 2

#define VAL_123_A _BV(0)
#define VAL_123_B _BV(1)
#define VAL_123_CLR _BV(2)
#define VAL_123_Q _BV(4)
#define VAL_123_NQ _BV(3)

// trig and notrig conditions

static const __flash uint8_t trigs_121[] = {
	VAL_121_B |          0 |          0,
	VAL_121_B |          0 | VAL_121_A1,
	VAL_121_B | VAL_121_A2 |          0,
	LAST_TRIG
};

static const __flash uint8_t notrigs_121[] = {
	        0 |          0 |          0,
	        0 |          0 | VAL_121_A1,
	        0 | VAL_121_A2 |          0,
	        0 | VAL_121_A2 | VAL_121_A1,
	// trigs go here
	VAL_121_B | VAL_121_A2 | VAL_121_A1,
	LAST_TRIG
};

static const __flash uint8_t trigs_122[] = {
	VAL_122_CLR | VAL_122_B2 | VAL_122_B1 |          0 |          0,
	VAL_122_CLR | VAL_122_B2 | VAL_122_B1 |          0 | VAL_122_A1,
	VAL_122_CLR | VAL_122_B2 | VAL_122_B1 | VAL_122_A2 |          0,
	LAST_TRIG
};

static const __flash uint8_t notrigs_122[] = {
	          0 |          0 |          0 |          0 |          0,
	          0 |          0 |          0 |          0 | VAL_122_A1,
	          0 |          0 |          0 | VAL_122_A2 |          0,
	          0 |          0 |          0 | VAL_122_A2 | VAL_122_A1,
	          0 |          0 | VAL_122_B1 |          0 |          0,
	          0 |          0 | VAL_122_B1 |          0 | VAL_122_A1,
	          0 |          0 | VAL_122_B1 | VAL_122_A2 |          0,
	          0 |          0 | VAL_122_B1 | VAL_122_A2 | VAL_122_A1,
	          0 | VAL_122_B2 |          0 |          0 |          0,
	          0 | VAL_122_B2 |          0 |          0 | VAL_122_A1,
	          0 | VAL_122_B2 |          0 | VAL_122_A2 |          0,
	          0 | VAL_122_B2 |          0 | VAL_122_A2 | VAL_122_A1,
	          0 | VAL_122_B2 | VAL_122_B1 |          0 |          0,
	          0 | VAL_122_B2 | VAL_122_B1 |          0 | VAL_122_A1,
	          0 | VAL_122_B2 | VAL_122_B1 | VAL_122_A2 |          0,
	          0 | VAL_122_B2 | VAL_122_B1 | VAL_122_A2 | VAL_122_A1,
	VAL_122_CLR |          0 |          0 |          0 |          0,
	VAL_122_CLR |          0 |          0 |          0 | VAL_122_A1,
	VAL_122_CLR |          0 |          0 | VAL_122_A2 |          0,
	VAL_122_CLR |          0 |          0 | VAL_122_A2 | VAL_122_A1,
	VAL_122_CLR |          0 | VAL_122_B1 |          0 |          0,
	VAL_122_CLR |          0 | VAL_122_B1 |          0 | VAL_122_A1,
	VAL_122_CLR |          0 | VAL_122_B1 | VAL_122_A2 |          0,
	VAL_122_CLR |          0 | VAL_122_B1 | VAL_122_A2 | VAL_122_A1,
	VAL_122_CLR | VAL_122_B2 |          0 |          0 |          0,
	VAL_122_CLR | VAL_122_B2 |          0 |          0 | VAL_122_A1,
	VAL_122_CLR | VAL_122_B2 |          0 | VAL_122_A2 |          0,
	VAL_122_CLR | VAL_122_B2 |          0 | VAL_122_A2 | VAL_122_A1,
	// trigs go here
	VAL_122_CLR | VAL_122_B2 | VAL_122_B1 | VAL_122_A2 | VAL_122_A1,
	LAST_TRIG
};

static const __flash uint8_t trigs_123[] = {
	VAL_123_CLR | VAL_123_B |         0,
	LAST_TRIG
};

static const __flash uint8_t notrigs_123[] = {
	          0 |         0 |         0,
	          0 |         0 | VAL_123_A,
	          0 | VAL_123_B |         0,
	          0 | VAL_123_B | VAL_123_A,
    VAL_123_CLR |         0 |         0,
	VAL_123_CLR |         0 | VAL_123_A,
	// trigs go here
	VAL_123_CLR | VAL_123_B | VAL_123_A,
	LAST_TRIG
};

// device-specific test variables

static const __flash struct univib_test {
	volatile uint8_t *port_trig;
	volatile uint8_t *pin_q;
	volatile uint8_t *pin_nq;
	uint8_t val_trig;
	uint8_t val_notrig;
	uint8_t val_clear;
	uint8_t val_q, val_nq;
	uint8_t trig_loops;
	const __flash uint8_t *trigs;
	const __flash uint8_t *notrigs;
} univib_test[4] = {
	{ // 74121
		.port_trig = &PORTC,
		.pin_q = &PINC,
		.pin_nq = &PINC,
		.val_trig = VAL_121_B,
		.val_notrig = VAL_121_A1 | VAL_121_A2,
		.val_clear = 0,
		.val_q = VAL_121_Q,
		.val_nq = VAL_121_NQ,
		.trig_loops = 1,
		.trigs = trigs_121,
		.notrigs = notrigs_121,
	},
	{ // 74122
		.port_trig = &PORTC, 
		.pin_q = &PINB, 
		.pin_nq = &PINC, 
		.val_trig = VAL_122_B1 | VAL_122_B2 | VAL_122_CLR, 
		.val_notrig = VAL_122_A1 | VAL_122_A2 | VAL_122_CLR, 
		.val_clear = VAL_122_A1 | VAL_122_A2, 
		.val_q = VAL_122_Q, 
		.val_nq = VAL_122_NQ, 
		.trig_loops = 6,
		.trigs = trigs_122,
		.notrigs = notrigs_122,
	},
	{ // 74123 univibrator 1
		.port_trig = &PORTC, 
		.pin_q = &PINB, 
		.pin_nq = &PINC, 
		.val_trig = VAL_123_B | VAL_123_CLR, 
		.val_notrig = VAL_123_A | VAL_123_CLR, 
		.val_clear = VAL_123_A, 
		.val_q = VAL_123_Q, 
		.val_nq = VAL_123_NQ, 
		.trig_loops = 6,
		.trigs = trigs_123,
		.notrigs = notrigs_123,
	},
	{ // 74123 univibrator 2
		.port_trig = &PORTB,
		.pin_q = &PINC,
		.pin_nq = &PINB,
		.val_trig = VAL_123_B | VAL_123_CLR,
		.val_notrig = VAL_123_A | VAL_123_CLR,
		.val_clear = VAL_123_A,
		.val_q = VAL_123_Q,
		.val_nq = VAL_123_NQ,
		.trig_loops = 6,
		.trigs = trigs_123,
		.notrigs = notrigs_123,
	},
};

// NOTE: The trick to keep compiler optimizations in check and
//       ensure proper test timings is to make sure 'uvt'
//       can be resolved to a constant during compilation time.
//       This makes the whole device/test selection logic dirty with all
//       the (duplicated) switch/case statements and inlined test functions,
//       but I'm afraid it's the only sensible way.

// -----------------------------------------------------------------------
static inline void trig(const __flash struct univib_test *uvt, uint8_t val)
{
	*uvt->port_trig = val;
	_NOP(); _NOP();
	*uvt->port_trig = uvt->val_notrig;
}

// -----------------------------------------------------------------------
static inline void clear(const __flash struct univib_test *uvt)
{
	*uvt->port_trig = uvt->val_clear;
	_NOP(); _NOP();
}

// -----------------------------------------------------------------------
static inline bool is_active(const __flash struct univib_test *uvt)
{
	if ((*uvt->pin_q & uvt->val_q) || !(*uvt->pin_nq & uvt->val_nq)) {
		return true;
	}
	return false;
}

// -----------------------------------------------------------------------
static inline bool is_other_active(const __flash struct univib_test *uvt)
{
	if ((*uvt->pin_nq & uvt->val_q) || !(*uvt->pin_q & uvt->val_nq)) {
		return true;
	}
	return false;
}

// -----------------------------------------------------------------------
static inline bool is_not_active(const __flash struct univib_test *uvt)
{
	if (!(*uvt->pin_q & uvt->val_q) || (*uvt->pin_nq & uvt->val_nq)) {
		return true;
	}
	return false;
}

// -----------------------------------------------------------------------
static inline uint8_t test_no_trig(const __flash struct univib_test *uvt)
{
	const __flash uint8_t *i = uvt->notrigs;

	while (*i != LAST_TRIG) {
		trig(uvt, *i);
		_NOP(); _NOP();
		if (is_active(uvt)) return RESP_FAIL;
		i++;
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t test_crosstrig(const __flash struct univib_test *uvt)
{
	const __flash uint8_t *i = uvt->trigs;

	while (*i != LAST_TRIG) {
		trig(uvt, *i);
		if (is_other_active(uvt)) return RESP_FAIL;
		_NOP(); _NOP(); _NOP();
		// ~500ns after the trigger
		if (is_other_active(uvt)) return RESP_FAIL;
		_delay_us(1.3);
		// ~2us after the last trigger
		if (is_other_active(uvt)) return RESP_FAIL;
		i++;
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t test_trig(const __flash struct univib_test *uvt)
{
	const __flash uint8_t *i = uvt->trigs;

	while (*i != LAST_TRIG) {
		trig(uvt, *i);
		// right after the trigger
		if (is_not_active(uvt)) return RESP_FAIL;
		_NOP(); _NOP(); _NOP();
		// ~500ns after the trigger
		if (is_not_active(uvt)) return RESP_FAIL;
		_delay_us(1.3);
		// ~2us after the last trigger
		if (is_active(uvt)) return RESP_FAIL;
		i++;
	}

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t test_retrig(const __flash struct univib_test *uvt)
{
	for (uint8_t i=0 ; i<uvt->trig_loops ; i++) {
		trig(uvt, uvt->val_trig);
		if (is_not_active(uvt)) return RESP_FAIL;
		_NOP(); _NOP(); _NOP();
		// ~500ns after the trigger
		if (is_not_active(uvt)) return RESP_FAIL;
	}
	_delay_us(1.3);
	// ~2us after the last trigger
	if (is_active(uvt)) return RESP_FAIL;

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static inline uint8_t test_clear(const __flash struct univib_test *uvt)
{
	trig(uvt, uvt->val_trig);
	if (is_not_active(uvt)) return RESP_FAIL;
	clear(uvt);
	if (is_active(uvt)) return RESP_FAIL;

	return RESP_PASS;
}

// -----------------------------------------------------------------------
static uint8_t test_121(uint8_t test)
{
	switch (test) {
		case TEST_NOTRIG: return test_no_trig(univib_test + UNIVIB_121);
		case TEST_TRIG: return test_trig(univib_test + UNIVIB_121);
		default: return RESP_ERR;
	}
}

// -----------------------------------------------------------------------
static uint8_t test_122(uint8_t test)
{
	switch (test) {
		case TEST_NOTRIG: return test_no_trig(univib_test + UNIVIB_122);
		case TEST_TRIG: return test_trig(univib_test + UNIVIB_122);
		case TEST_RETRIG: return test_retrig(univib_test + UNIVIB_122);
		case TEST_CLEAR: return test_clear(univib_test + UNIVIB_122);
		default: return RESP_ERR;
	}
}

// -----------------------------------------------------------------------
static uint8_t test_123_1(uint8_t test)
{
	switch (test) {
		case TEST_NOTRIG: return test_no_trig(univib_test + UNIVIB_123_1);
		case TEST_TRIG: return test_trig(univib_test + UNIVIB_123_1);
		case TEST_RETRIG: return test_retrig(univib_test + UNIVIB_123_1);
		case TEST_CLEAR: return test_clear(univib_test + UNIVIB_123_1);
		case TEST_CROSSTRIG: return test_crosstrig(univib_test + UNIVIB_123_1);
		default: return RESP_ERR;
	}
}

// -----------------------------------------------------------------------
static uint8_t test_123_2(uint8_t test)
{
	switch (test) {
		case TEST_NOTRIG: return test_no_trig(univib_test + UNIVIB_123_2);
		case TEST_TRIG: return test_trig(univib_test + UNIVIB_123_2);
		case TEST_RETRIG: return test_retrig(univib_test + UNIVIB_123_2);
		case TEST_CLEAR: return test_clear(univib_test + UNIVIB_123_2);
		case TEST_CROSSTRIG: return test_crosstrig(univib_test + UNIVIB_123_2);
		default: return RESP_ERR;
	}
}

// -----------------------------------------------------------------------
uint8_t run_univib(uint8_t *params)
{
	uint8_t device = params[PARAM_DEV];
	uint8_t test = params[PARAM_TEST];

	switch (device) {
		case UNIVIB_121: return test_121(test);
		case UNIVIB_122: return test_122(test);
		case UNIVIB_123_1: return test_123_1(test);
		case UNIVIB_123_2: return test_123_2(test);
		default: return RESP_ERR;
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
