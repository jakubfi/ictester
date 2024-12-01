from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

class Part74180(PackageDIP14):
    name = "74180"
    desc = "9-bit odd/even parity generator/checker"
    pin_cfg = {
        1: Pin("G", PinType.IN),
        2: Pin("H", PinType.IN),
        3: Pin("EVEN", PinType.IN),
        4: Pin("ODD", PinType.IN),
        5: Pin("sumEVEN", PinType.OUT),
        6: Pin("sumODD", PinType.OUT),
        8: Pin("A", PinType.IN),
        9: Pin("B", PinType.IN),
        10: Pin("C", PinType.IN),
        11: Pin("D", PinType.IN),
        12: Pin("E", PinType.IN),
        13: Pin("F", PinType.IN),
    }

    default_inputs = [8, 9, 10, 11, 12, 13, 1, 2,  3, 4]
    default_outputs = [5, 6]

    test_valid_even = TestLogic("Even upstream", default_inputs, default_outputs,
        loops=64,
        body=lambda: [[[*data, 1, 0],  [data.even(), data.odd()]] for data in BV.range(0, 256)]
    )
    test_valid_odd = TestLogic("Odd upstream", default_inputs, default_outputs,
        loops=64,
        body=lambda: [[[*data, 0, 1],  [data.odd(), data.even()]] for data in BV.range(0, 256)]
    )
    test_invalid = TestLogic("Invalid upstream", default_inputs, default_outputs,
        loops=64,
        body=lambda: [
            [[*data, *even_odd], ~BV(even_odd)]
            for data in BV.range(0, 256)
            for even_odd in [[1, 1], [0, 0]]
        ]
    )

    tests = [test_valid_even, test_valid_odd, test_invalid]
