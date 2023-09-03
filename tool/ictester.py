#!/usr/bin/env python3

import sys
import argparse
import math
import re

from tester import Tester
from transport import Transport
from parts import catalog


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
# --- Main ---------------------------------------------------------------
# ------------------------------------------------------------------------

FAIL = '\033[91m\033[1m'
OK = '\033[92m\033[1m'
WARN = '\033[95m\033[1m'
SKIP = '\033[93m\033[1m'
ENDC = '\033[0m'

if '--list' in sys.argv:
    list_parts("--tests" in sys.argv)
    sys.exit(0)

parser = argparse.ArgumentParser(description='IC tester controller')
parser.add_argument('--device', default="/dev/ttyUSB1", help='Serial port where the IC tester is connected')
parser.add_argument('--loops', type=int, default=None, help='Loop count (1..65535)')
parser.add_argument('--delay', type=float, default=None, help='additional DUT output read delay in μs for logic tests (13107 μs max, rounded to nearest 0.2 μs)')
parser.add_argument('--list', action="store_true", help='List all supported parts')
parser.add_argument('--tests', action="store_true", help='When listing parts, list also tests for each part')
parser.add_argument('--debug', action="store_true", help='Enable debug output')
parser.add_argument('--debug-serial', action="store_true", help='Enable serial debug output')
parser.add_argument('part', help='Part symbol')
args = parser.parse_args()

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

transport = Transport(args.device, 500000, debug=args.debug_serial)
tester = Tester(part, transport, debug=args.debug)
all_tests = tester.tests_available()
test_count = len(all_tests)
longest_desc = len(max(all_tests, key=len))

tests_failed = 0
total_time = 0

tester.dut_setup()

for test_name in all_tests:
    test = tester.part.get_test(test_name)
    loops = args.loops if args.loops is not None else test.loops

    plural = "s" if loops != 1 else ""
    endc = "\n" if args.debug else ""
    stats = f"({len(test.vectors)} vectors, {loops} loop{plural})"
    print(f" * Testing: {test_name:{longest_desc}s}   {stats:25}  ... ", end=endc, flush=True)

    if tests_failed:
        print(f"\b\b\b\b{SKIP}SKIPPED{ENDC}")
    else:
        res, elapsed = tester.exec_test(test, loops, args.delay)
        if res == Tester.RESP_PASS:
            print(f"\b\b\b\b{OK}PASS{ENDC}  ({elapsed:.2f} sec.)")
        else:
            tests_failed += 1
            print(f"\b\b\b\b{FAIL}FAIL{ENDC}  ({elapsed:.2f} sec.)")

tester.dut_disconnect()

if tests_failed != 0:
    result = f"{FAIL}PART DEFECTIVE"
    ret = 1
else:
    result = f"{OK}PART OK"
    ret = 0

print(f"\n{result}{ENDC}")

sys.exit(ret)
