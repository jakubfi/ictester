#include <util/delay.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <limits.h>

#include "ina.h"
#include "isense.h"
#include "protocol.h"

static struct resp_logic_imeasure imeas;

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

// -----------------------------------------------------------------------
void clear_current_stats()
{
	imeas.max_ivcc.ivcc = 0;
	imeas.max_ivcc.ignd = 0;
	imeas.max_ignd.ivcc = 0;
	imeas.max_ignd.ignd = 0;
	imeas.min_ivcc.ivcc = SHRT_MAX;
	imeas.min_ivcc.ignd = SHRT_MAX;
	imeas.min_ignd.ivcc = SHRT_MAX;
	imeas.min_ignd.ignd = SHRT_MAX;
	imeas.min_vbus = USHRT_MAX;
}

// -----------------------------------------------------------------------
void update_current_stats()
{
	int16_t ivcc, ignd;
	uint16_t vbus;

	isense_all(&vbus, &ivcc, &ignd);
	if (ivcc > imeas.max_ivcc.ivcc) { imeas.max_ivcc.ivcc = ivcc; imeas.max_ivcc.ignd = ignd; }
	if (ignd > imeas.max_ignd.ignd) { imeas.max_ignd.ivcc = ivcc; imeas.max_ignd.ignd = ignd; }
	if (ivcc < imeas.min_ivcc.ivcc) { imeas.min_ivcc.ivcc = ivcc; imeas.min_ivcc.ignd = ignd; }
	if (ignd < imeas.min_ignd.ignd) { imeas.min_ignd.ivcc = ivcc; imeas.min_ignd.ignd = ignd; }
	if (vbus < imeas.min_vbus) { imeas.min_vbus = vbus; }
}

// -----------------------------------------------------------------------
uint16_t store_current_stats(uint8_t *buf)
{
	const uint8_t count = 2*2*4 + 2;
	memcpy(buf, &imeas, count);
	return count;
}

// vim: tabstop=4 shiftwidth=4 autoindent
