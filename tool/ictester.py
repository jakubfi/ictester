#!/usr/bin/env python3.8

import sys
import argparse
import math

from tester import Tester
import parts

# ------------------------------------------------------------------------
# --- Main ---------------------------------------------------------------
# ------------------------------------------------------------------------

FAIL = '\033[91m\033[1m'
OK = '\033[92m\033[1m'
ENDC = '\033[0m'

if '--list' in sys.argv:
    names = sorted(parts.catalog.keys(), key=int)
    for name in names:
        p = parts.catalog[name]
        print("{} ({}): {}".format(p.name, p.package_name, p.desc))
    sys.exit(0)

parser = argparse.ArgumentParser(description='IC tester controller')
parser.add_argument('--device', default="/dev/ttyUSB1", help='Serial port where the IC tester is connected')
parser.add_argument('--loops', type=int, help='Loop count (<65536, will be rounded to the nearest power of 2)')
parser.add_argument('--list', action="store_true", help='List all supported parts')
parser.add_argument('--debug', action="store_true", help='Enable debug output')
parser.add_argument('--serial_debug', action="store_true", help='Enable serial debug output')
parser.add_argument('part', help='Part symbol')
args = parser.parse_args()

try:
    part = parts.catalog[args.part]
except KeyError:
    print("Part not found: {}".format(args.part))
    print("Use --list to list all supported parts")
    sys.exit(1)

print("Testing {}-pin part {}: {}, package {}...".format(part.pincount, part.name, part.desc, part.package_name))

tester = Tester(part, args.device, 500000, debug=args.debug, serial_debug=args.serial_debug)
all_tests = tester.tests_available()
longest_desc = len(max(all_tests, key=len))
failed = False
tests_passed = 0

for test_name in all_tests:
    test = tester.part.get_test(test_name)
    loops = args.loops if args.loops is not None else test.loops
    loops_pow = round((math.log2(loops)))
    loops = 2 ** loops_pow

    if not args.debug:
        print(" * {:{}s}  ({} loop{}) ".format(
            test_name,
            longest_desc,
            loops,
            "s" if loops != 1 else ""
        ), end='', flush=True)
    else:
        print(" * {} ({} loop{})".format(
            test_name, loops,
            "s" if loops != 1 else ""
        ))

    res = tester.run(test, loops_pow)

    if res == Tester.RES_PASS:
        tests_passed += 1
        print("{}PASS{}".format(OK, ENDC))
    else:
        failed = True
        print("{}FAIL{}".format(FAIL, ENDC))

if tests_passed != len(tester.tests_available()):
    color = FAIL
    result = "FAILED"
    ret = 1
else:
    color = OK
    result = "OK"
    ret = 0

print("{}{}: {} of {} tests passed{}".format(color, result, tests_passed, len(tester.tests_available()), ENDC))

sys.exit(ret)
