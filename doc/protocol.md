__WARNING: protocol is not yet finalized nor fully implemented__

# Overview

Dialog between the software and the tester are conducted using messages. There are two types of messages:

 * commands,
 * responses.

Dialog is always initiated with a command sent by the software controlling the tester. Tester always responds with a response.

All BYTES are unsigned. All WORDS are unsigned 16-bit values, little-endian.

## Available commands

| Command              | Value | Description                                       |
|----------------------|-------|---------------------------------------------------|
| `CMD_HELLO`          | 1     | Check comms and get tester information            |
| `CMD_DUT_SETUP`      | 2     | Configure tester for the DUT                      |
| `CMD_DUT_POWERUP`    | 3     | Power up the DUT                                  |
| `CMD_TEST_SETUP`     | 4     | Setup the test                                    |
| `CMD_VECTORS_LOAD`   | 5     | Load test vectors (optional, if used by the test) |
| `CMD_TEST_RUN`       | 6     | Run the test                                      |
| `CMD_DUT_DISCONNECT` | 7     | Power down the DUT, disconnect from the tester    |

## Available responses

| Response             | Value | Meaning                                |
|----------------------|-------|----------------------------------------|
| `RESP_HELLO`         | 128   | Tester information                     |
| `RESP_OK`            | 129   | Command executed                       |
| `RESP_PASS`          | 130   | Test finished successfully             |
| `RESP_FAIL`          | 131   | Test finished with failure             |
| `RESP_ERR`           | 132   | Error                                  |
| `RESP_TIMING_ERROR`  | 133   | Test finished with read timing error   |


# Command description


## Hello

To verify that controlling software can work with the hardware, initial "Hello" handshake has to be performed.

### Command format

* 1 BYTE: command `CMD_HELLO`

### Valid responses

Tester always responds with `RESP_HELLO`, described in later section.


## DUT Setup

Before any other command, tester needs to be set up for the specific DUT.
This command informs the tester how to address DUT pins and sets ZIF socket pin functions for the DUT.
Protocol allows sending 1 or 2 pin configurations when setting up the DUT. One configuration is used
in most cases. Two configurations are required for DUTs with bidirectional pins, where pin roles
change from test to test.

### Command format

* 1 BYTE: command: `CMD_DUT_SETUP`
* 1 BYTE: `t` = package type (1=DIP)
* 1 BYTE: `p` = number of all DUT pins ([14, 16, 20, 24])
* 1 BYTE: `c` = number of pin configurations (min 1, max 4)
* `c` PIN CONFIGURATIONS (internally numbered starting from `0`):
  * `p` BYTES: `p` ZIF pin functions for each DUT pin. 1 byte each, starting from pin 1. See table below.

| ZIF Function        | Value | MCU Pin Function          | SW Function      | Default DUT use            |
|---------------------|-------|---------------------------|------------------|----------------------------|
| `ZIF_OUT`           | 1     | output                    | -                | TTL input                  |
| `ZIF_IN_HIZ`        | 2     | input HiZ                 | -                | TTL output, not connected  |
| `ZIF_IN_PU_STRONG`  | 3     | input HiZ                 | pull-up 4.7 kΩ   | open-collector output      |
| `ZIF_IN_PU_WEAK`    | 4     | input with weak pullup    | -                | TTL output, 3-state output |
| `ZIF_OUT_SINK`      | 5     | output driven low (sink)  | -                | open-emitter               |
| `ZIF_C`             | 6     | input HiZ                 | capacitor 470 pF | univibrator C connection   |
| `ZIF_OUT_SOURCE`    | 7     | output driven high (sink) | -                | -                          |
| `ZIF_VCC`           | 128   | input HiZ                 | VDUT (+5 V)      | VCC (+5 V)                 |
| `ZIF_GND`           | 129   | input HiZ                 | GND              | GND                        |

### Valid responses

* `RESP_OK` - DUT configuration accepted
* `RESP_ERR` - DUT configuration not accepted


## DUT Power Up

This command causes the tester to apply power to the DUT. Requires the DUT to be set up first.

DUT connection is done in 3 steps:

* connect GND and VCC pins,
* apply power to the VCC pin
* measure GND and VCC current and bus voltage

If measured current exceeds 190mA, overcurrent is reported and DUT is disconnected.

### Command format

* 1 BYTE: command: `CMD_DUT_POWERUP`
* 1 BYTE: safety\_off: 1=disable overcurrent check, 0=check for overcurrent

### Valid responses

* `RESP_OK` - DUT connected
* `RESP_ERR` - DUT cannot be connected


## DUT Disconnect

This command causes the tester to power down the DUT and deconfigure it's pin connections.
Note that DUT is also immediately disconnected by the tester if a test fails.

DUT disconnection is done in 3 steps:

* disconnect power to the DUT
* disconnect VCC, GND, pull-ups and C pins,
* drain charges from DUT pins and bypass caps
* deconfigure MCU pins (set all pins as HiZ)

### Command format

* 1 BYTE: command: `CMD_DUT_DISCONNECT`

### Valid responses

* `RESP_OK` - DUT disconnected


## Test Setup

Sets up the test. Requires the DUT to be set up first.

### Command format

* 1 BYTE: command: `CMD_TEST_SETUP`
* 1 BYTE: DUT pin configuration number used by the test
  (configuration `0` is available for every DUT, more may be available in some cases. See `CMD_DUT_SETUP`)
* 1 BYTE: test type. Algorithm used to test the DUT. See table below for test types available.
* TEST PARAMETERS: depend on the test type, see below.

| Test type           | Value | Description                                                             |
|---------------------|-------|-------------------------------------------------------------------------|
| `TEST_LOGIC`        | 1     | Logic ICs. Designed for 74 family, but suitable for other families too  |
| `TEST_DRAM`         | 2     | 4164 and 41256 DRAM memories                                            |
| `TEST_UNIVIB`       | 3     | 74121, 74122 and 74123 monostable monovibrators                         |

### Valid responses

* `RESP_OK` - test setup successfull
* `RESP_ERR` - test setup failed

### Test types

Available test types and their specific requirements are described below.

#### Logic IC test

`TEST_LOGIC` (1) is designed to test 74 logic (both combinatorial and sequential), but suitable for many other IC families.
It's a basic, generic test that uses test vectors (uploaded with a separate command) to verify IC functionality by
setting its inputs to given values and checking if IC outputs match test vector outputs.

Test parameters:

* 1 WORD: additional delay (in 200 ns units) before checking DUT outputs. 0 for no delay.
* `n` BYTES: I/O pin usage in test vectors (n=2 for 14-pin and 16-pin devices, n=3 for >16-pin devices):
  * each bit: 1=I/O pin used by the test, 0=pin not used by the test
  * 1st byte contains lowest pin numbers, bit 0 in each byte describes pin with the lowest number

#### 4164 and 41256 DRAM memory test

`TEST_DRAM` (2) is designed to test 4164 and 41256 DRAM memory chips. There are three tests available, all using MARCH C- algorithm:

* read-modify-write - test is done using read-modify-write memory access,
* read+write - test is done using separate "read" and "write" operations,
* page mode - test is done using page reads and writes, treating the whole page as a single word.

Test parameters:

* 1 BYTE: tested device:
  * 1 = 4164 (64kbit),
  * 2 = 41256 (256kbit).
* 1 BYTE: test type:
  * 1 = read-modify-write,
  * 2 = read+write,
  * 3 = page mode.

#### 7412x univibrator test

`TEST_UNIVIB` (3) is designed to test 74121, 74122 and 74123 univibrators. Test does not use vectors and uses the following parameters:

* 1 BYTE: tested device:
  * 0 = 74121,
  * 1 = 74122,
  * 2 = 74123 univibrator 1,
  * 3 = 74123 univibrator 2
* 1 BYTE: test type:
  * 0 = conditions which should not trigger the device
  * 1 = conditions that should trigger the device
  * 2 = retrigger (not available for 74121)
  * 3 = clear (not available for 74121)
  * 4 = cross-trigger check (only for 74123)
  * 5 = trigger with rising clear edge (not available for 74121)

## Vectors upload

Upload test vectors. Requires the test to be set up first. Test needs to use vectors.

### Command format

* 1 BYTE: command: `CMD_VECTORS_LOAD`
* 1 WORD: `v` = number of test vectors, >0.
* `v` VECTORS

Each vector consists of 2 (for <=16-pin devices) or 3 (for >16-pin devices) BYTES.
Each byte contains bit values for 8 consecutive DUT pins.
For each input, bit value is set on DUT input. For each output, bit value is compared to DUT output. Bits map to pins as follow:

```
        .----.----.----.----.----.----.----.----.
BYTE 1: |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |
        +----.----.----.----.----.----.----.----+
BYTE 2: | 16 | 15 | 14 | 13 | 12 | 11 | 10 |  9 |
        +----.----.----.----.----.----.----.----+
BYTE 3: | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | (only for >16-pin devices)
        `----`----`----`----`----`----`----`----`
```

* Pins absent in the tested device are ignored (eg. for 14-pin devices two most significant bits of BYTE 2 are ignored).
* Non-I/O pins and pins not declared as inputs or outpus in the test are ignored, with one **exception** described below.

**Bit for VCC pin has a special meaning.**
Since it's never set nor read, tester uses it to decide whether DUT outputs should be checked at all.
If VCC pin is set to "1" for a given vector, test result for this vector is not checked.
Such vectors are used for DUT state setup and in sequential logic tests, where output has to be checked
only after the clock/strobe input changes.

### Valid responses

* `RESP_OK` - vectors uploaded successfully
* `RESP_ERR` - vector upload failed

## Run Test

Run the uploaded test. Requires test to be set and vectors to be uploaded (if required by the test).
If the test fails, DUT is immediately disconnected.

### Command format

* 1 BYTE: command: `CMD_TEST_RUN`
* 1 WORD: number of loops, 0 for infinite testing.

### Valid responses

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

This response is sent when command has been successfully executed.

* 1 BYTE: response: `RESP_OK`

## Command error

This response is sent when a command cannot be executed or the execution failed.

* 1 BYTE: response: `RESP_ERR`
* 1 BYTE: error code from the table below

| Command                    | Value | Description                                       |
|----------------------------|-------|---------------------------------------------------|
| `ERR_UNKNOWN`              | 0     | Error code was not set (likely a software bug)    |
| `ERR_CMD_UNKNOWN`          | 1     | Unknown command                                   |
| `ERR_CMD_TOOBIG`           | 2     | Command didn't fit in the receive buffer          |
| `ERR_CRC`                  | 3     | CRC transmission error detected                   |
|                            | 4     | (unused)                                          |
| `ERR_PACKAGE`              | 5     | Unsupported package type                          |
| `ERR_PIN_CNT`              | 6     | Unsupported pin count                             |
| `ERR_PIN_FUNC`             | 7     | Unknown pin function                              |
| `ERR_PIN_COMB`             | 8     | Bad pin function combination (eg. VCC+GND)        |
|                            | 9     | (unused)                                          |
| `ERR_TEST_TYPE`            | 10    | Unsupported test type                             |
|                            | 11    | (unused)                                          |
| `ERR_VECT_NUM`             | 12    | Wrong number of test vectors (<1 or too many)     |
| `ERR_PINCFG_CNT`           | 13    | Wrong pin configuration count                     |
| `ERR_PINCFG_NUM`           | 14    | Wrong pin configuration number (config not set)   |
|                            | 15    | (unused)                                          |
| `ERR_PIN_FUNC_UNAVAILABLE` | 16    | Function not available for a pin                  |
| `ERR_NO_PINCFG`            | 17    | No pin configuration active                       |
| `ERR_UNKNOWN_CHIP`         | 18    | Selected chip type is unknown                     |
| `ERR_UNKNOWN_TEST`         | 19    | No such test for selected chip                    |
| `ERR_OVERCURRENT`          | 20    | Overcurrent detected while connecting DUT         |

## Test PASS

This response is sent only for `CMD_TEST_RUN` command, when the test passes successfully.

* 1 BYTE: response: `RESP_PASS`

## Test FAIL

This response is sent only for `CMD_TEST_RUN` command, when the test fails.
Note that when test fails, DUT is immediately disconnected by the tester.

* 1 BYTE: response: `RESP_FAIL`
* FAILURE DESCRIPTION. Depends on the test type, see below.

### `TEST_LOGIC` failure

  * 1 WORD: vector number that test failed on
  * `n` bytes of pin data - failing vector. 2 or 3 bytes, format as for the pin mask in the test configuration.

### `TEST_DRAM` failure

  * 1 WORD: failing row address
  * 1 WORD: failing column address
  * 1 BYTE: failing MARCH C- step

### `TEST_UNIVIB` failure

Test sends no additional description.

## Test timing error

This response is sent only for `CMD_TEST_RUN` command and indicates output read timing error.
5 μs after the initial test vector failure, vector is tested again. If that second check
passes, `RESP_TIMING_ERROR` is sent in response. Otherwise test fails with `RESP_FAIL`.

* 1 BYTE: response: `RESP_TIMING_ERROR`


