from binvec import BV
from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part74S405(PackageDIP16):
    name = "74S405"
    desc = "1-from-8 binary decoder"
    pin_cfg = {
        1: Pin("A0", PinType.IN),
        2: Pin("A1", PinType.IN),
        3: Pin("A2", PinType.IN),
        4: Pin("~E1", PinType.IN),
        5: Pin("~E2", PinType.IN),
        6: Pin("E3", PinType.IN),
        7: Pin("O7", PinType.OUT),
        9: Pin("O6", PinType.OUT),
        10: Pin("O5", PinType.OUT),
        11: Pin("O4", PinType.OUT),
        12: Pin("O3", PinType.OUT),
        13: Pin("O2", PinType.OUT),
        14: Pin("O1", PinType.OUT),
        15: Pin("O0", PinType.OUT),
    }

    default_inputs = [4, 5, 6,  3, 2, 1]
    default_outputs = [7, 9, 10, 11, 12, 13, 14, 15]

    test_select = TestLogic("Select", default_inputs, default_outputs,
        body=[[[0, 0, 1, *BV.int(i, 3)],  ~BV.bit(i, 8)] for i in range(0, 8)]
    )
    test_inhibit = TestLogic("Inhibit (all comb.)", default_inputs, default_outputs,
        body=[[[*BV.int(i, 3), 0, 0, 0],  8*[1]] for i in set(range(0, 8)) - {1}]
    )

    tests = [test_select, test_inhibit]
