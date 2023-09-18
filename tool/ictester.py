#!/usr/bin/env python3

import sys
import argparse
import math
import re
import difflib
import logging
import serial.tools.list_ports as listports
from serial.serialutil import SerialException

from tester import (Resp, Tester)
from prototypes import TestType
from transport import Transport
from parts import catalog

FAIL = '\033[91m\033[1m'
OK = '\033[92m\033[1m'
WARN = '\033[95m\033[1m'
SKIP = '\033[93m\033[1m'
HI = '\033[97m\033[1m'
ENDC = '\033[0m'

result_color = {
    Resp.HELLO: OK,
    Resp.OK: OK,
    Resp.PASS: OK,
    Resp.FAIL: FAIL,
    Resp.ERR: FAIL,
    Resp.TIMING_ERROR: WARN,
    Resp.SKIP: SKIP,
}

logging.basicConfig(format='%(message)s', level=logging.CRITICAL)
logger = logging.getLogger('ictester')

# ------------------------------------------------------------------------
def print_parts(list_tests=False):
    families = {}
    for i in catalog.items():
        family = i[0][0:2]
        if family not in families:
            families[family] = []
        families[family].append(i)

    for family, parts in sorted(families.items()):
        for name, part in sorted(parts, key=lambda x: int(re.sub("74[HSL]+", "74", x[0]))):
            print(f"{name:7s} {part.package_name:6s} {part.desc}")
            if (list_tests):
                for t in part.tests:
                    print(f"  * {t.name} ({len(t.vectors)} vectors)")

# ------------------------------------------------------------------------
def print_part_info(part):
    print(f"Part: {part.name}, {part.package_name} - {part.desc}")
    if part.missing_tests:
        print(f"{WARN}WARNING: missing tests: {part.missing_tests}{ENDC}")

# ------------------------------------------------------------------------
def print_vector_chunk(prefix, vector, widths, vector_other=None, color=""):
    print(prefix, end="")
    for n, i in enumerate(vector):
        bitcolor = FAIL if vector_other and i != vector_other[n] else color
        print(f"{bitcolor}{str(i):>{widths[n]+1}}{ENDC}", end="")

# ------------------------------------------------------------------------
def print_vector(label, inputs, outputs, i_width, o_width, i_other=None, o_other=None, color="", separator=""):
    print_vector_chunk(f" {HI}{label:<5}{ENDC}", inputs, i_width, i_other, color)
    print_vector_chunk(separator.center(5), outputs, o_width, o_other, color)
    print()

# ------------------------------------------------------------------------
def print_failed_vector(part, test, failed_vector_num, failed_pin_vector, context=3):
    i_failed = [int(failed_pin_vector[pin-1]) for pin in test.inputs]
    o_failed = [int(failed_pin_vector[pin-1]) for pin in test.outputs]

    i_names = [part.pins[pin].name for pin in test.inputs]
    o_names = [part.pins[pin].name for pin in test.outputs]

    i_width = [len(x) for x in i_names]
    o_width = [len(x) for x in o_names]

    print()
    start_vec = max(failed_vector_num - context, 0)
    print_vector("", i_names, o_names, i_width, o_width, color=HI, separator="->")
    for i in range(start_vec, failed_vector_num+1):
        inputs = [int(x) for x in test.vectors[i].input]
        outputs = [int(x) for x in test.vectors[i].output]
        if i != failed_vector_num:
            print_vector(f"{i}:", inputs, outputs, i_width, o_width)
        else:
            print_vector(f"{i}:", i_failed, o_failed, i_width, o_width, inputs, outputs)
    print()

# ------------------------------------------------------------------------
def parse_cmd():
    # check early to not require "part" argument
    if '--list-all' in sys.argv or '--list' in sys.argv:
        print_parts(list_tests='--list-all' in sys.argv)
        sys.exit(0)

    parser = argparse.ArgumentParser(description='IC tester controller')
    parser.add_argument('-d', '--device', default=None, help='Serial port where the IC tester is connected')
    parser.add_argument('-l', '--loops', type=int, default=None, help='Loop count (1..65535)')
    parser.add_argument('-t', '--test', type=int, default=None, help='Test number to run')
    parser.add_argument('-D', '--delay', type=float, default=None, help='additional DUT output read delay in μs for logic tests (13107 μs max, rounded to nearest 0.2 μs)')
    parser.add_argument('-L', '--list', action="store_true", help='List all supported parts')
    parser.add_argument('-A', '--list-all', action="store_true", help='List all supported parts and all tests for each part')
    parser.add_argument('-v', '--verbose', action="count", default=0, help='Verbose output. Twice for even more verbosity')
    parser.add_argument('part', help='Part symbol')
    args = parser.parse_args()

    if args.verbose > 1:
        logger.setLevel(logging.DEBUG)
    elif args.verbose > 0:
        logger.setLevel(logging.INFO)

    if args.test is not None and args.test <= 0:
        parser.error("Test numbers start from 1")

    if args.loops is not None and (args.loops <= 0 or args.loops > 65535):
        parser.error("Loops should be between 1 and 65535")

    if args.delay is not None and (args.delay < 0 or args.delay > 13107):
        parser.error("Delay should be between 0 and 13107")

    return args

# ------------------------------------------------------------------------
def get_part(part_name):
    try:
        part = catalog[part_name]
    except KeyError:
        print(f"Part \"{part_name}\" not found. Use --list to list all supported parts.")
        matches = difflib.get_close_matches(part_name, catalog, n=1, cutoff=0.7)
        if matches:
            matches = ', '.join(matches)
            print(f"Supported part with the most similar name is: {HI}{matches}{ENDC}")
        sys.exit(100)
    return part

# ------------------------------------------------------------------------
def get_serial_port(device):
    # Try searching for ictester
    detected_device = None
    for port in listports.comports():
        if port.manufacturer == "mera400.pl" and port.product == "ictester":
            detected_device = port.device

    serial_port = device if device else detected_device

    # Device not found
    if not serial_port:
        print("No ictester found. Please specify device with --device argument.")
        sys.exit(90)

    return serial_port

# ------------------------------------------------------------------------
# --- Main ---------------------------------------------------------------
# ------------------------------------------------------------------------

args = parse_cmd()
part = get_part(args.part.upper())
serial_port = get_serial_port(args.device)

try:
    transport = Transport(serial_port, 500000)
except SerialException as e:
    print(f"Could not open connection to the tester: {e}")
    sys.exit(80)
tester = Tester(part, transport)
tester.dut_setup()

if args.test:
    try:
        run_tests = [part.tests[args.test-1]]
    except IndexError:
        print(f"Test number {args.test} is not available for {part.name}")
        sys.exit(70)
else:
    run_tests = part.tests

longest_desc = max(len(t.name) for t in run_tests)

total_time = 0

print_part_info(part)
print()

for test in run_tests:
    loops = args.loops if args.loops is not None else test.loops

    plural = "s" if loops != 1 else ""
    stats = f"({len(test.vectors)} vectors, {loops} loop{plural})"
    endc = "\n" if logger.isEnabledFor(logging.INFO) else ""
    print(f" * Testing: {test.name:{longest_desc}s}   {stats:25}  ... ", end=endc, flush=True)

    if not tester.failed:
        resp, elapsed = tester.exec_test(test, loops, args.delay)
    else:
        resp = Resp.SKIP

    print(f"\b\b\b\b{result_color[resp]}{resp.name}{ENDC}", end="")
    if resp in (Resp.PASS, Resp.FAIL):
        print(f"  ({elapsed:.2f} sec.)", end="")
    print()

    if resp == Resp.FAIL:
        if test.type == TestType.LOGIC:
            failed_vector_num, failed_pin_vector = tester.get_failed_vector()
            print_failed_vector(part, test, failed_vector_num, failed_pin_vector)

# required only on success, but just in case do it always
tester.dut_disconnect()

if resp != Resp.FAIL:
    print()

tests_skipped = len(part.tests) - (tester.failed + tester.warning + tester.passed)

print(f"Total tests: {HI}{len(run_tests)}{ENDC}", end="")
if tester.failed:
    print(f", failed: {FAIL}{tester.failed}{ENDC}", end="")
if tester.warning:
    print(f", warning: {WARN}{tester.warning}{ENDC}", end="")
if tests_skipped:
    print(f", skipped: {SKIP}{tests_skipped}{ENDC}", end="")
if tester.passed:
    print(f", passed: {OK}{tester.passed}{ENDC}", end="")
print()

if tester.failed:
    result = f"{FAIL}PART DEFECTIVE"
    ret = 1
elif tester.warning:
    result = f"{WARN}OUTPUT READ TIMING ERROR"
    ret = 2
else:
    result = f"{OK}PART OK"
    ret = 0

print(f"{result}{ENDC}")

sys.exit(ret)
