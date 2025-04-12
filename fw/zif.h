#ifndef __ZIF_H__
#define __ZIF_H__

#include <inttypes.h>

#define ZIF_PIN_CNT 24

// NOTE: ZIF port mapping is not entirely abstracted away.
//       Two functions in dram.c: addr_low() and addr_high()
//       require manual adjusting.

// ZIF ports to MCU port numbers (indices for mcu_config), 0-based
#define ZIF_PORT_0 0
#define ZIF_PORT_1 1
#define ZIF_PORT_2 2
// ZIF ports to MCU DDRs
#define ZIF_MCU_DDR_0 DDRC
#define ZIF_MCU_DDR_1 DDRA
#define ZIF_MCU_DDR_2 DDRB
// ZIF ports to MCU PORTs
#define ZIF_MCU_PORT_0 PORTC
#define ZIF_MCU_PORT_1 PORTA
#define ZIF_MCU_PORT_2 PORTB
// ZIF ports to MCU PINs
#define ZIF_MCU_PIN_0 PINC
#define ZIF_MCU_PIN_1 PINA
#define ZIF_MCU_PIN_2 PINB

// ZIF pins to MCU port bits, 0-based
// on ZIF_PORT_0
#define ZIF_0_PORT_BIT 7
#define ZIF_1_PORT_BIT 6
#define ZIF_2_PORT_BIT 5
#define ZIF_3_PORT_BIT 4
#define ZIF_4_PORT_BIT 3
#define ZIF_5_PORT_BIT 2
#define ZIF_6_PORT_BIT 1
#define ZIF_7_PORT_BIT 0
// on ZIF_PORT_1
#define ZIF_8_PORT_BIT 7
#define ZIF_9_PORT_BIT 6
#define ZIF_10_PORT_BIT 5
#define ZIF_11_PORT_BIT 4
#define ZIF_12_PORT_BIT 3
#define ZIF_13_PORT_BIT 2
#define ZIF_14_PORT_BIT 1
#define ZIF_15_PORT_BIT 0
// on ZIF_PORT_2
#define ZIF_16_PORT_BIT 7
#define ZIF_17_PORT_BIT 6
#define ZIF_18_PORT_BIT 5
#define ZIF_19_PORT_BIT 4
#define ZIF_20_PORT_BIT 3
#define ZIF_21_PORT_BIT 2
#define ZIF_22_PORT_BIT 1
#define ZIF_23_PORT_BIT 0


void zif_init();
uint8_t zif_pos(uint8_t dut_pin_count, uint8_t dut_pin);
bool zif_func(uint8_t func, uint8_t zif_pin);
bool zif_power_up(uint16_t *vbus, int16_t *ivcc, int16_t *ignd, bool safty_off);
void zif_config_select(uint8_t cfgnum);
bool zif_connect();
void zif_disconnect();
void zif_config_clear();
uint8_t zif_get_vcc_pin();

uint8_t zif_mcu_port(uint8_t zif_pin);
uint8_t zif_mcu_port_bit(uint8_t zif_pin);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
