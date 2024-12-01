from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74S201(PackageDIP16):
    name = "74S201"
    desc = "256-bit high-performance random-access memory"
    pin_cfg = {
        1: Pin("A0", PinType.IN),
        2: Pin("A1", PinType.IN),
        3: Pin("~S1", PinType.IN),
        4: Pin("~S2", PinType.IN),
        5: Pin("~S3", PinType.IN),
        6: Pin("~Q", PinType.OC),
        7: Pin("A3", PinType.IN),
        9: Pin("A4", PinType.IN),
        10: Pin("A5", PinType.IN),
        11: Pin("A6", PinType.IN),
        12: Pin("R/~W", PinType.IN),
        13: Pin("D", PinType.IN),
        14: Pin("A7", PinType.IN),
        15: Pin("A2", PinType.IN),
    }

    # ------------------------------------------------------------------------
    @staticmethod
    def for_all_addr(op, s1, s2, s3, i, o):
        return [
            [[op, s1, s2, s3, *addr, i], [o]]
            for addr in BV.range(0, 256)
        ]

    default_inputs = [12,  3, 4, 5,  1, 2, 15, 7, 9, 10, 11, 14,  13]
    default_outputs = [6]

    test_rw = TestLogic("R/W all address space", default_inputs, default_outputs,
        loops=32,
        body=lambda: Part74S201.for_all_addr(0,  0, 0, 0,  0,  1)  # write '0', output = high impedance
            + Part74S201.for_all_addr(1,  0, 0, 0,  0,  1)  # read, output = '1'
            + Part74S201.for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + Part74S201.for_all_addr(1,  0, 0, 0,  0,  0)  # read, output = '0'
    )
    test_inhibit_read = TestLogic("Inhibit read", default_inputs, default_outputs,
        loops=32,
        body=lambda: Part74S201.for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + Part74S201.for_all_addr(1,  0, 0, 1,  0,  1)  # inhibit read, output = high impedance
            + Part74S201.for_all_addr(1,  0, 1, 0,  0,  1)  # inhibit read, output = high impedance
            + Part74S201.for_all_addr(1,  1, 0, 0,  0,  1)  # inhibit read, output = high impedance
    )
    test_inhibit_write = TestLogic("Inhibit write", default_inputs, default_outputs,
        loops=32,
        body=lambda: Part74S201.for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + [[[1, 1, 1, 1,  0, 0, 0, 0, 0, 0, 0, 0,  0], [1]]]  # set inhibit
            + Part74S201.for_all_addr(0,  1, 1, 1,  0,  1)  # inhibit write '1', output = high impedance
            + Part74S201.for_all_addr(1,  0, 0, 0,  0,  0)  # inhibit read, output = 0
    )

    tests = [test_rw, test_inhibit_read, test_inhibit_write]
