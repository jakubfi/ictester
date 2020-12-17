#!/usr/bin/env python3.8

import sys
import argparse

from tester import Tester
import parts

# ------------------------------------------------------------------------
# --- Main ---------------------------------------------------------------
# ------------------------------------------------------------------------

if '--list' in sys.argv:
    for name, p in parts.catalog.items():
        print("{} ({}): {}".format(p.name, p.package_name, p.desc))
    sys.exit(0)

parser = argparse.ArgumentParser(description='IC tester controller')
parser.add_argument('--device', default="/dev/ttyUSB1", help='Serial port where the IC tester is connected')
parser.add_argument('--speed', default="19200", help='Port speed')
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
tester = Tester(part, args.device, args.speed, debug=args.debug)
for test_name in tester.tests_available():
    if not args.debug:
        print("Running test: {}... ".format(test_name), end='', flush=True)
    else:
        print("Running test: {}... ".format(test_name))
    res = tester.run(test_name, args.loop_pow)
    if res == Tester.RES_PASS:
        print("PASS")
    else:
        print("FAIL")
