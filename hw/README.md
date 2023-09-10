KiCad project files for Logic IC Tester.

See also [pdf schematic](../doc/ictester.pdf)

# Connectors and jumpers

* J1, J2, J3, J4 - debug connectors. Duplicate ZIF socket connections (plus additional GND connections) and allow
  connecting external measurement equipment. Can also be used for testing ICs and circuits outside the ZIF socket.
* JP1 - jumper shorting +5V to DUT power supply lines. Normally closed. Can be used for measuring IC current
  or for supplying the IC with external power.
* J6 - external USB UART module connection. Use only if the onboart USB UART is not populated.
* J7 - free MCU PD7 connection, ground and +5V.
* J8 - MCU programmer interface.

# CP2102N setup

To complete the hardware setup, CP2102N USB UART transceiver needs to be programmed with the following values:

* iManufacturer = mera400.pl
* iProduct = ictester
* MaxPower = 200mA

One possible way of programming it is to use [this](https://github.com/VCTLabs/cp210x-program/tree/master/ext/badge) tool:

`cp2102 -p "ictester" -m "mera400.pl" -x 200`

You can also use one of the tools provided by the manufacturer - Silicon Labs.

This step is not required, although without it no device autodetection will be possible and in some cases the default power limit (100 mA) may be too low.

# BOM

| Ref  | Value/Part | Package
|------|-------|---------|
| C1, C3, C6, C7, C10-C14, C18 | 100n | 0805
| C2, C4	| 22p | 0805
| C5 | 1u	| 0805
| C8 | 10u | EIA-3528 Kemet-B
| C9, C15-C17 | 470p | 0805
| J1+J3, J2+J4 | goldpin 01x14 | 2.54mm pitch
| J6 | goldpin 01x06 | 2.54mm pitch
| J7 | goldpin 01x04 | 2.54mm pitch
| J8 | goldpin 02x05 | 2.54mm pitch
| J9 | Amphenol 10104110 | USB B Micro
| JP1 | Jumper 1x02 | 2.54mm pitch
| LED1 | Inolux IN-PI554FCH
| R1 | 10k | 0805
| R2-R29 | 4k7 | 0805
| U1 | ATmega1284 | TQFP-44 10x10mm
| U2 | CP2102N | QFN28	5x5mm
| U3 | RClamp0504F | EIAJ SC-70 6L
| U4-U8 | MAX14662 | QFN28 4x4mm
| U9 | ZIF24 Socket |
| Y1 | Abracon ABM3C 20MHz |
