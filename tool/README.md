# Logic IC Tester Control Software

This software communincates with the logic IC tester using [binary protocol](../doc/protocol.md) over a serial connection.
It first sets up all the DUT connections according to IC pin description and then runs tests for the selected IC.

For the time being there is no packaged version available.
Tool requires python >=3.6 and `pyserial` to work.

# Usage

To list supported ICs use `./ictester.py --list`. Additional `--tests` option will also list all tests for each part.

To run tests for selected part use: `./ictester.py [--device DEVICE] [--loops LOOPS] part`.
Default device is `/dev/ttyUSB0`. Number of test loops can be set between 1 and 65535.
Additional `--debug` and `--debug-serial` options may help when debugging problems with the software.

Apart from the program output, tester hardware signals its state with a status LED:

* white - tester powered up and ready
* yellow - DUT connected, test session running (do not remove the DUT from the socket)
* green - last test session finished with success (part is OK)
* red - last test session finished with failure (part is defective)
* purple - error encountered during session run
