from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

# like 74151, different pinout

class Part9312(PackageDIP16):
    name = "9312"
    desc = "One of Eight Line Data Selectors/Multiplexers"
    pin_cfg = {
        1: Pin("D0", PinType.IN),
        2: Pin("D1", PinType.IN),
        3: Pin("D2", PinType.IN),
        4: Pin("D3", PinType.IN),
        5: Pin("D4", PinType.IN),
        6: Pin("D5", PinType.IN),
        7: Pin("D6", PinType.IN),
        9: Pin("D7", PinType.IN),
        10: Pin("~G", PinType.IN),
        11: Pin("A", PinType.IN),
        12: Pin("B", PinType.IN),
        13: Pin("C", PinType.IN),
        14: Pin("W", PinType.OUT),
        15: Pin("Y", PinType.OUT),
    }

    default_inputs = [9, 7, 6, 5, 4, 3, 2, 1,  13, 12, 11,  10]
    default_outputs = [15, 14]

    tests = [
        TestLogic("Select 0", default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 0],  [0, 1]] for addr in range(0, 8)]
        ),
        TestLogic("Select 1", default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 0],  [1, 0]] for addr in range(0, 8)]
        ),
        TestLogic("Inhibit 0", default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 1],  [0, 1]] for addr in range(0, 8)]
        ),
        TestLogic("Inhibit 1", default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 1],  [0, 1]] for addr in range(0, 8)]
        )
    ]

