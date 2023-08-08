__WARNING: protocol is not yet finalized nor fully implemented__

# Overview

Dialog between the software and the tester are conducted using messages. There are two types of messages:

 * commands,
 * responses.


Dialog is always initiated with a command sent by the software controlling the tester. Tester always responds with a response.

Available commands:

| Command              | Value | Description                                       |
|----------------------|-------|---------------------------------------------------|
| `CMD_HELLO`          | 1     | Check comms and get tester information            |
| `CMD_DUT_SETUP`      | 2     | Configure tester for the DUT                      |
| `CMD_DUT_CONNECT`    | 3     | Connect the DUT to the tester, power it up        |
| `CMD_TEST_SETUP`     | 4     | Setup the test                                    |
| `CMD_VECTORS_LOAD`   | 5     | Load test vectors (optional, if used by the test) |
| `CMD_TEST_RUN`       | 6     | Run the test                                      |
| `CMD_DUT_DISCONNECT` | 7     | Power down the DUT, disconnect from the tester    |

Available responses:

| Response             | Value | Meaning                       |
|----------------------|-------|-------------------------------|
| `RESP_HELLO`         | 128   | Tester information            |
| `RESP_OK`            | 129   | Command executed              |
| `RESP_PASS`          | 130   | Test finished successfully    |
| `RESP_FAIL`          | 131   | Test finished with failure    |
| `RESP_ERR`           | 132   | Error                         |


# Commands


## Hello

To verify that controlling software can work with the hardware, initial "Hello" handshake has to be performed.

* 1 BYTE: command `CMD_HELLO`

Tester always responds with `RESP_HELLO`, described in later section.


## DUT Setup

Before any other command, tester needs to be set up for the specific DUT.
This command informs the tester how to address DUT pins and sets ZIF socket pin functions for the DUT.

* 1 BYTE: command: `CMD_DUT_SETUP`
* 1 BYTE: `t` = package type  (1=DIP)
* 1 BYTE: `p` = number of all DUT pins ([14, 16, 20, 24])
* `p` BYTES: `p` ZIF pin functions for each DUT pin. 1 byte each, starting from pin 1. See table below.

| ZIF Function        | Value | MCU Pin Function               | SW Function      | Default DUT use            |
|---------------------|-------|--------------------------------|------------------|----------------------------|
| `ZIF_OUT`           | 1     | output                         | -                | TTL input                  |
| `ZIF_IN`            | 2     | input                          | -                | TTL output                 |
| `ZIF_IN_PU_STRONG`  | 3     | input                          | pull-up 4k7      | open-collector output      |
| `ZIF_IN_PU_WEAK`    | 4     | input with weak pullup (>100k) | -                | 3-state output             |
| `ZIF_OUT_SINK`      | 5     | output driven low (sink)       | -                | open-emitter               |
| `ZIF_C`             | 6     | high impedance                 | capacitor 470p   | univibrator C connection   |
| `ZIF_OUT_SOURCE`    | 7     | output driven high (sink)      | -                | -                          |
| `ZIF_VCC`           | 128   | high impedance                 | VDUT (+5V)       | +5V                        |
| `ZIF_GND`           | 129   | high impedance                 | GND              | GND                        |
| `ZIF_HIZ`           | 255   | high impedance                 | -                | not connected, unused      |

Valid responses:

* `RESP_OK` - DUT configuration accepted
* `RESP_ERR` - DUT configuration not accepted


## DUT Connect

This command causes the tester to configure it's pin connections and apply power to the DUT. Requires the DUT to be set up first.
DUT connect starts the test session; tests can be loaded and executed one by one.

* 1 BYTE: command: `CMD_DUT_CONNECT`

Valid responses:

* `RESP_OK` - DUT connected
* `RESP_ERR` - DUT cannot be connected


## DUT Disconnect

This command causes the tester to power down the DUT and deconfigure it's pin connections.
Disconnect ends the test session.

* 1 BYTE: command: `CMD_DUT_DISCONNECT`

Valid responses:

* `RESP_OK` - DUT disconnected


## Test Setup

Sets up the test. Requires the DUT to be set up first.

* 1 BYTE: command: `CMD_TEST_SETUP`
* 1 BYTE: test type. Algorithm used to test the DUT. See below for test types available.
* 4 BYTES: test parameters `PARAM_1` - `PARAM_4`. Sent and received even if test does not use them.
* `n` BYTES: I/O pin usage in test vectors (n=2 for 14-pin and 16-pin devices, n=3 for >16-pin devices):
    * each bit: 1=I/O pin used by the test, 0=pin not used by the test
    * 1st byte - lowest pin numbers
    * bit 0 in each byte - lowest pin number

Valid responses:

* `RESP_OK` - test setup successfull
* `RESP_ERR` - test setup failed

### Logic IC test

Designed to test 74 logic (both combinatorial and sequential), but suitable for many other IC families.

  * `TEST_LOGIC` (1)
    * does not use (ignores) test parameters
    * requires test vectors

### 4164 and 41256 DRAM memory test

  * `TEST_DRAM_41` (2)
    * uses following test parameters:
      * `PARAM_1` - memory size: 1=64k (4164), 2=256k (41256)
      * `PARAM_2` - test type: 1=read-modify-write, 2=read+write, 3=page mode
    * does not use test vectors


## Vectors upload

Upload test vectors. Requires the test to be set up first. Test needs to use vectors.

* 1 BYTE: command: `CMD_VECTORS_LOAD`
* 2 BYTES: `v` = number of test vectors (little-endian), >0.
* `v` VECTORS, each containing all pin values (inputs to set, outputs to check):
  * 1 BYTE: check result (0=no, otherwise=yes)
  * `n` BYTES: pin data (n=2 for 14-pin and 16-pin devices, n=3 for >16-pin devices)
    * 1st byte - lowest pin numbers
    * bit 0 in each byte - lowest pin number
    * bits for pins other than used by the test are ignored
    * DUT inputs are set according to input pin bits
    * DUT outputs are checked against output bits if result checking is enabled for the vector

Valid responses:

* `RESP_OK` - vectors uploaded successfully
* `RESP_ERR` - vector upload failed

## Run Test

Run the uploaded test. Requires test to be set and vectors to be uploaded (if required by the test).

* 1 BYTE: command: `CMD_TEST_RUN`
* 2 BYTES: `l` = number of loops, "0" for infinite testing (little-endian).

Valid responses:

* `RESP_ERR` - not possible to execute the test
* `RESP_PASS` - test executed, passed
* `RESP_FAIL` - test executed, failed


# Responses

## Hello

* 1 BYTE: `RESP_HELLO`
* 1 BYTE: protocol version
* 1 BYTE: firmware version
* 6 BYTES: reserved, unused but always sent and received

If protocol version reported by the hardware differs from protocol version supported
by the software, software refuses operation.
If firmware version is lower than supported by the software, operation can continue,
but not all tests available in the software can be run..
If firmware version is higher than supported by the software, operation can continue,
but not all features available in the hardware may be available to the software.

## Command OK

* 1 BYTE: response: `RESP_OK`

## Command error

* 1 BYTE: response: `RESP_ERR`
* 1 BYTE: error code from the table below

| Command         | Value | Description                                       |
|-----------------|-------|---------------------------------------------------|
| `ERR_UNKNOWN`   | 0     | Error code was not set (likely a bug)             |
| `ERR_CMD`       | 1     | Unknown command                                   |
| `ERR_NO_SETUP`  | 2     | Missing DUT setup                                 |
| `ERR_NO_TEST`   | 3     | No test set                                       |
| `ERR_NO_VECT`   | 4     | No vectors loaded                                 |
| `ERR_PACKAGE`   | 5     | Unsupported package type                          |
| `ERR_PIN_CNT`   | 6     | Unsupported pin count                             |
| `ERR_PIN_FUNC`  | 7     | Unknown pin function                              |
| `ERR_PIN_COMB`  | 8     | Bad pin function combination (eg. VCC+GND)        |
| `ERR_PIN_SETUP` | 9     | Unsupported pin setup                             |
| `ERR_TEST_TYPE` | 10    | Unsupported test type                             |
| `ERR_PARAMS`    | 11    | Bad test parameters                               |
| `ERR_VECT_NUM`  | 12    | Wrong number of test vectors (<1 or too many)     |

## Test PASS

* 1 BYTE: response: `RESP_PASS`

## Test FAIL

* 1 BYTE: response: `RESP_FAIL`
* `x` BYTES: failure description. Depends on the test type:
  * `TEST_LOGIC`
    * 2 BYTES: vector number that test failed on (little-endian)
    * `n` bytes of pin data - failing vector. Format as in the test configuration.
  * `TEST_DRAM_41`
    * 2 BYTES: failing address (little endian)
    * 1 BYTE: failing MARCH step
