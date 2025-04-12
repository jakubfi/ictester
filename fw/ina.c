#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>
#include <util/delay.h>

#include "external/fleury-i2cmaster/i2cmaster_a.h"
#include "external/fleury-i2cmaster/i2cmaster_b.h"

#include "ina.h"

const __flash struct isense_drv {
	void (*i2c_start_wait)(unsigned char);
	unsigned char (*i2c_rep_start)(unsigned char);
	void (*i2c_stop)(void);
	unsigned char (*i2c_write)(unsigned char);
	unsigned char (*i2c_readAck)(void);
	unsigned char (*i2c_readNak)(void);
	uint8_t i2c_addr;
} isense_drv[2] = {
	{
		// low side
		i2c_a_start_wait,
		i2c_a_rep_start,
		i2c_a_stop,
		i2c_a_write,
		i2c_a_readAck,
		i2c_a_readNak,
		0b10000000
	},
	{
		// high side
		i2c_b_start_wait,
		i2c_b_rep_start,
		i2c_b_stop,
		i2c_b_write,
		i2c_b_readAck,
		i2c_b_readNak,
		0b10000010
	},
};

// -----------------------------------------------------------------------
void ina_init()
{
	i2c_a_init();
	i2c_b_init();
}

// -----------------------------------------------------------------------
uint16_t ina_read(uint8_t dev, uint8_t reg)
{
	const __flash struct isense_drv *ina = isense_drv + dev;
	uint16_t val;

	ina->i2c_start_wait(ina->i2c_addr + I2C_A_WRITE);
	ina->i2c_write(reg);
	ina->i2c_rep_start(ina->i2c_addr + I2C_A_READ);
	val = ina->i2c_readAck() << 8;
	val |= ina->i2c_readNak();
	ina->i2c_stop();

	return val;
}

// -----------------------------------------------------------------------
void ina_write(uint8_t dev, uint8_t reg, uint16_t val)
{
	const __flash struct isense_drv *ina = isense_drv + dev;

	ina->i2c_start_wait(ina->i2c_addr + I2C_A_WRITE);
	ina->i2c_write(reg);
	ina->i2c_write(val >> 8);
	ina->i2c_write(val & 0xff);
	ina->i2c_stop();
}

// vim: tabstop=4 shiftwidth=4 autoindent
