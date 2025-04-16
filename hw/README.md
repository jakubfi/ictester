KiCad project files for Logic IC Tester.

See also [pdf schematic](../doc/ictester.pdf)

# Connectors and jumpers

* J1, J2, J3, J4 - debug connectors. Duplicate ZIF socket connections (plus additional GND connections) and allow
  connecting external measurement equipment. Can also be used for testing ICs and circuits outside the ZIF socket.
* J5 - MCU programmer interface.
* J6 - USB port
* J7 - jumper shorting +5V to DUT power supply lines. Normally closed. Can be used for measuring IC current
  or for supplying the IC with external power.

# CP2102N setup

To complete the hardware setup, CP2102N USB UART transceiver needs to be programmed with the following values:

* iManufacturer = mera400.pl
* iProduct = ictester
* MaxPower = 200mA

One possible way of programming it is to use [this](https://github.com/VCTLabs/cp210x-program/tree/master/ext/badge) tool:

`cp2102 -p "ictester" -m "mera400.pl" -x 200`

You can also use one of the tools provided by the manufacturer - Silicon Labs.

This step is not required, although without it no device autodetection will be possible.
