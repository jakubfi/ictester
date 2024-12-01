from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74155(PackageDIP16):
    name = "74155"
    desc = "Dual 2-line to 4-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("1C", PinType.IN),
        2: Pin("~1G", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("1Y3", PinType.OUT),
        5: Pin("1Y2", PinType.OUT),
        6: Pin("1Y1", PinType.OUT),
        7: Pin("1Y0", PinType.OUT),
        9: Pin("2Y0", PinType.OUT),
        10: Pin("2Y1", PinType.OUT),
        11: Pin("2Y2", PinType.OUT),
        12: Pin("2Y3", PinType.OUT),
        13: Pin("A", PinType.IN),
        14: Pin("~2G", PinType.IN),
        15: Pin("~2C", PinType.IN),
    }

    default_inputs = [3, 13,  2, 1,  14, 15]
    default_outputs = [4, 5, 6, 7,  12, 11, 10, 9]

    test_inhibit = TestLogic("Inhibit", default_inputs, default_outputs,
        body=[
            [[*addr, 1, data, 1, data],  8*[1]]
            for addr in BV.range(0, 4)
            for data in [0, 1]
        ]
    )
    test_select_0 = TestLogic("Select 0", default_inputs, default_outputs,
        body=[
            [[*BV.int(addr, 2), 0, 0,  0, 0],  [1, 1, 1, 1, *~BV.bit(addr, 4)]] for addr in range(0, 4)
        ]
    )
    test_select_1 = TestLogic("Select 1", default_inputs, default_outputs,
        body=[
            [[*BV.int(addr, 2), 0, 1,  0, 1],  [*~BV.bit(addr, 4), 1, 1, 1, 1]] for addr in range(0, 4)
        ]
    )

    tests = [test_select_0, test_select_1, test_inhibit]
