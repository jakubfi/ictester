#ifndef __ISENSE_H__
#define __ISENSE_H__

#define SHUNT_190_MA 15200  // 190 mA / (2.5 uV / 0.2 ohm)

void isense_init();
uint16_t isense_vbus_vcc();
uint16_t isense_vbus_gnd();
int16_t isense_shunt_vcc();
int16_t isense_shunt_gnd();
void isense_all(uint16_t *vbus, int16_t *ivcc, int16_t *ignd);
void clear_current_stats();
void update_current_stats();
uint16_t store_current_stats(uint8_t *buf);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent

