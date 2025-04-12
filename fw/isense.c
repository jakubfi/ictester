#include <util/delay.h>

#include "ina.h"
#include "isense.h"

// -----------------------------------------------------------------------
void isense_init()
{
	uint16_t ina_cfg = INA_CFG_ADC_HI
		| INA_CFG_AVG_1
		| INA_CFG_VBUSCT_140
		| INA_CFG_VSHCT_140
		| INA_CFG_MODE_CON_BUS_SH;

	ina_init();
	ina_write(I_HI, INA_REG_CFG, ina_cfg);
	ina_write(I_LO, INA_REG_CFG, ina_cfg);
}

// -----------------------------------------------------------------------
uint16_t isense_vbus_vcc()
{
	_delay_us(280);
	return ina_read(I_HI, INA_REG_BUS) & 0x7fff;
}

// -----------------------------------------------------------------------
uint16_t isense_vbus_gnd()
{
	_delay_us(280);
	return ina_read(I_LO, INA_REG_BUS) & 0x7fff;
}

// -----------------------------------------------------------------------
int16_t isense_shunt_vcc()
{
	_delay_us(280);
	return ina_read(I_HI, INA_REG_SHUNT);
}

// -----------------------------------------------------------------------
int16_t isense_shunt_gnd()
{
	_delay_us(280);
	return ina_read(I_LO, INA_REG_SHUNT);
}

// -----------------------------------------------------------------------
void isense_all(uint16_t *vbus, int16_t *ivcc, int16_t *ignd)
{
	_delay_us(280);
	*vbus = ina_read(I_HI, INA_REG_BUS) & 0x7fff;
	*ivcc = ina_read(I_HI, INA_REG_SHUNT);
	*ignd = ina_read(I_LO, INA_REG_SHUNT);
}

// vim: tabstop=4 shiftwidth=4 autoindent
