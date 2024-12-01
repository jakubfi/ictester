from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74153(PackageDIP16):
    name = "74153"
    desc = "Dual 4-line to 1-line data selectors/multiplexers"
    pin_cfg = {
        1: Pin("~1G", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("1C3", PinType.IN),
        4: Pin("1C2", PinType.IN),
        5: Pin("1C1", PinType.IN),
        6: Pin("1C0", PinType.IN),
        7: Pin("1Y", PinType.OUT),
        9: Pin("2Y", PinType.OUT),
        10: Pin("2C0", PinType.IN),
        11: Pin("2C1", PinType.IN),
        12: Pin("2C2", PinType.IN),
        13: Pin("2C3", PinType.IN),
        14: Pin("A", PinType.IN),
        15: Pin("~2G", PinType.IN),
    }

    default_inputs = [2, 14,  1,  3, 4, 5, 6,  15,  13, 12, 11, 10]
    default_outputs = [7, 9]

    test_select_0 = TestLogic("Select 0", default_inputs, default_outputs,
        body=[[[*BV.int(addr, 2), *(2*[0, *~BV.bit(addr, 4)])],  [0, 0]] for addr in range(0, 4)]
    )
    test_select_1 = TestLogic("Select 1", default_inputs, default_outputs,
        body=[[[*BV.int(addr, 2), *(2*[0, *BV.bit(addr, 4)])],  [1, 1]] for addr in range(0, 4)]
    )
    test_inhibit_0 = TestLogic("Inhibit 0", default_inputs, default_outputs,
        body=[[[*addr, *(2*[1, 0, 0, 0, 0])],  [0, 0]] for addr in BV.range(0, 4)]
    )
    test_inhibit_1 = TestLogic("Inhibit 1", default_inputs, default_outputs,
        body=[[[*addr, *(2*[1, 1, 1, 1, 1])],  [0, 0]] for addr in BV.range(0, 4)]
    )

    tests = [test_select_0, test_select_1, test_inhibit_0, test_inhibit_1]
