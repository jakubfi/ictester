#!/usr/bin/env python3.8

import sys
import argparse

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
parser.add_argument('--loop_pow', default=10, type=int, choices=range(0, 16), help='Loop count power (2^loop_pow)')
parser.add_argument('--list', action="store_true", help='List all supported parts')
parser.add_argument('--debug', action="store_true", help='Enable debug output')
parser.add_argument('part', help='Part symbol')
args = parser.parse_args()

try:
    part = parts.catalog[args.part]
except KeyError:
    print("Part not found: {}".format(args.part))
    print("Use --list to list all supported parts")
    sys.exit(1)

print("Testing {}-pin part {}: {}, package {}...".format(part.pincount, part.name, part.desc, part.package_name))

tester = Tester(part, args.device, 500000, debug=args.debug)
all_tests = tester.tests_available()
longest_desc = len(max(all_tests, key=len))
failed = False
tests_passed = 0

for test_name in all_tests:
    if not args.debug:
        print(" * {:{n}s}".format(test_name, n=longest_desc+2), end='', flush=True)
    else:
        print(" * {} ".format(test_name))
    res = tester.run(test_name, args.loop_pow)
    if res == Tester.RES_PASS:
        tests_passed += 1
        print("{}PASS{}".format(OK, ENDC))
    else:
        failed = True
        print("{}FAIL{}".format(FAIL, ENDC))

if tests_passed != len(tester.tests_available()):
    color = FAIL
    result = "FAILED"
else:
    color = OK
    result = "OK"

print("{}{}: {} of {} tests passed{}".format(color, result, tests_passed, len(tester.tests_available()), ENDC))
