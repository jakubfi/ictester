#!/usr/bin/env python3

import sys
import argparse
import math
import re
import serial.tools.list_ports as listports

from tester import Tester
from transport import Transport
from parts import catalog

FAIL = '\033[91m\033[1m'
OK = '\033[92m\033[1m'
WARN = '\033[95m\033[1m'
SKIP = '\033[93m\033[1m'
HI = '\033[97m\033[1m'
ENDC = '\033[0m'


# ------------------------------------------------------------------------
def list_parts(list_tests=False):
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
                    print(f"  * ({len(t.vectors)} vectors) {t.name}")

# ------------------------------------------------------------------------
def print_part_info(part):
    print(f"Part: {part.name}, {part.package_name} - {part.desc}")
    if part.missing_tests:
        print(f"{WARN}WARNING: missing tests: {part.missing_tests}{ENDC}")

# ------------------------------------------------------------------------
def vector_chunk_print(prefix, vector, widths, vector_other=None, color=""):
    print(prefix, end="")
    for n, i in enumerate(vector):
        bitcolor = FAIL if vector_other and i != vector_other[n] else color
        print(f"{bitcolor}{str(i):>{widths[n]+1}}{ENDC}", end="")

# ------------------------------------------------------------------------
def vector_print(label, inputs, outputs, i_width, o_width, i_other=None, o_other=None, color="", separator=""):
    vector_chunk_print(f" {HI}{label:<5}{ENDC}", inputs, i_width, i_other, color)
    vector_chunk_print(separator.center(5), outputs, o_width, o_other, color)
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
    vector_print("", i_names, o_names, i_width, o_width, color=HI, separator="->")
    for i in range(start_vec, failed_vector_num+1):
        inputs = [int(x) for x in test.vectors[i].input]
        outputs = [int(x) for x in test.vectors[i].output]
        if i < failed_vector_num:
            vector_print(f"{i}:", inputs, outputs, i_width, o_width)
        else:
            vector_print(f"{i}:", i_failed, o_failed, i_width, o_width, inputs, outputs)
    print()


# ------------------------------------------------------------------------
# --- Main ---------------------------------------------------------------
# ------------------------------------------------------------------------

if '--list' in sys.argv:
    list_parts("--tests" in sys.argv)
    sys.exit(0)

parser = argparse.ArgumentParser(description='IC tester controller')
parser.add_argument('--device', default=None, help='Serial port where the IC tester is connected')
parser.add_argument('--loops', type=int, default=None, help='Loop count (1..65535)')
parser.add_argument('--delay', type=float, default=None, help='additional DUT output read delay in μs for logic tests (13107 μs max, rounded to nearest 0.2 μs)')
parser.add_argument('--list', action="store_true", help='List all supported parts')
parser.add_argument('--tests', action="store_true", help='When listing parts, list also tests for each part')
parser.add_argument('--debug', action="store_true", help='Enable debug output')
parser.add_argument('--debug-serial', action="store_true", help='Enable serial debug output')
parser.add_argument('part', help='Part symbol')
args = parser.parse_args()

# Try searching for ictester
detected_device = None
for port in listports.comports():
    if port.manufacturer == "mera400.pl" and port.product == "ictester":
        detected_device = port.device

serial_port = args.device if args.device else detected_device

# Device not found
if not serial_port:
    print("No ictester found. Please specify device with --device argument.")
    sys.exit(90)

if args.loops is not None and (args.loops <= 0 or args.loops > 65535):
    parser.error("Loops should be between 1 and 65535")

if args.delay is not None and (args.delay < 0 or args.delay > 13107):
    parser.error("Delay should be between 0 and 13107")

try:
    part = catalog[args.part.upper()]
except KeyError:
    print(f"Part not found: {args.part}")
    print("Use --list to list all supported parts")
    sys.exit(100)

print_part_info(part)
print()

transport = Transport(serial_port, 500000, debug=args.debug_serial)
tester = Tester(part, transport, debug=args.debug)
all_tests = tester.tests_available()
test_count = len(all_tests)
longest_desc = len(max(all_tests, key=len))

tests_failed = 0
tests_warning = 0
tests_skipped = 0
tests_passed = 0
total_time = 0

tester.dut_setup()

for test_name in all_tests:
    logic_fail_was_last = False
    test = tester.part.get_test(test_name)
    loops = args.loops if args.loops is not None else test.loops

    plural = "s" if loops != 1 else ""
    endc = "\n" if args.debug else ""
    stats = f"({len(test.vectors)} vectors, {loops} loop{plural})"
    print(f" * Testing: {test_name:{longest_desc}s}   {stats:25}  ... ", end=endc, flush=True)

    if tests_failed:
        tests_skipped += 1
        print(f"\b\b\b\b{SKIP}SKIP{ENDC}")
    else:
        res, elapsed, failed_vector_num, zif_vector = tester.exec_test(test, loops, args.delay)
        if res == Tester.RESP_PASS:
            tests_passed += 1
            print(f"\b\b\b\b{OK}PASS{ENDC}  ({elapsed:.2f} sec.)")
        elif res == Tester.RESP_TIMING_FAIL:
            tests_warning += 1
            print(f"\b\b\b\b{WARN}TIMING ERROR{ENDC}")
        elif res == Tester.RESP_FAIL:
            tests_failed += 1
            print(f"\b\b\b\b{FAIL}FAIL{ENDC}  ({elapsed:.2f} sec.)")
            if test.type == test.LOGIC:
                print_failed_vector(part, test, failed_vector_num, zif_vector)
                logic_fail_was_last = True
        else:
            tests_failed += 1
            print(f"\b\b\b\b{FAIL}FAIL{ENDC}  ({elapsed:.2f} sec.)")

tester.dut_disconnect()

if not logic_fail_was_last:
    print()

print(f"Total tests: {HI}{len(all_tests)}{ENDC}", end="")
if tests_failed:
    print(f", failed: {FAIL}{tests_failed}{ENDC}", end="")
if tests_warning:
    print(f", warning: {WARN}{tests_warning}{ENDC}", end="")
if tests_skipped:
    print(f", skipped: {SKIP}{tests_skipped}{ENDC}", end="")
if tests_passed:
    print(f", passed: {OK}{tests_passed}{ENDC}", end="")
print()

if tests_failed:
    result = f"{FAIL}PART DEFECTIVE"
    ret = 1
elif tests_warning:
    result = f"{WARN}OUTPUT READ TIMING ERROR"
    ret = 2
else:
    result = f"{OK}PART OK"
    ret = 0

print(f"{result}{ENDC}")

sys.exit(ret)
