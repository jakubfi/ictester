# Logic IC Tester Control Software

This software communincates with the logic IC tester using [binary protocol](../doc/protocol.md) over a serial connection.
It first sets up all the DUT connections according to IC pin description and then runs tests for the selected IC.


# Installation

For both Linux and Windows installation requirements are the same:

* `python` >=3.6
* `git`

Note for Windows users: both git and python need to be available in your PATH for the installation to work.

Optionally create a new virtual environment:
```
virtualenv ictester
. ictester/bin/activate
```

Install the package:
```
pip install -e "git+https://github.com/jakubfi/ictester/#egg=ictester&subdirectory=controller"
```
Alternatively, clone the repo manually and install:
```
git clone https://github.com/jakubfi/ictester
cd ictester/controller
pip install .
```

# Usage

To list supported ICs use: `ictester --list`. `--list-all` will also list all tests for each part.
To run tests for a selected part use: `ictester <part>`.
To display help, use `ictester --help`

Note for Windows users: you'll need Silicon Labs CP210x USB to UART Bridge Driver installed
for the communication with IC tester to work. Also, device autodetection may fail.
In such case, use `--device COMx` option.

Other options when running a test:

* `-d DEVICE` or `--device DEVICE` - Serial port where the IC tester is connected. Required only when autodetection fails for some reason.
* `-l LOOPS` or `--loops LOOPS` - Test loop count (1..65535)
* `-t TEST` or `--test TEST` - Selects specific test to run
* `-D DELAY` or `--delay DELAY` - additional DUT output read delay in μs (for logic tests only, 13107 μs max, rounded to nearest 0.2 μs)
* `-v` or `--verbose` - Verbose output. Repeat for even more verbosity.
* `--safety-off` - Test the DUT even if overcurrent condition is detected.

Apart from the program output, tester hardware signals its state with a status LED:

* white - tester powered up and ready
* amber - DUT connected, test session running (do not remove the DUT from the socket)
* green - last test session finished with success (part is OK)
* red - last test session finished with failure (part is defective)
* purple - error encountered during session run
