from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74151(PackageDIP16):
    name = "74151"
    desc = "Data selectors/multiplexers"
    pin_cfg = {
        1: Pin("D3", PinType.IN),
        2: Pin("D2", PinType.IN),
        3: Pin("D1", PinType.IN),
        4: Pin("D0", PinType.IN),
        5: Pin("Y", PinType.OUT),
        6: Pin("W", PinType.OUT),
        7: Pin("~G", PinType.IN),
        9: Pin("C", PinType.IN),
        10: Pin("B", PinType.IN),
        11: Pin("A", PinType.IN),
        12: Pin("D7", PinType.IN),
        13: Pin("D6", PinType.IN),
        14: Pin("D5", PinType.IN),
        15: Pin("D4", PinType.IN),
    }

    default_inputs = [12, 13, 14, 15, 1, 2, 3, 4,  9, 10, 11,  7]
    default_outputs = [5, 6]

    tests = [
        TestLogic("Select 0", default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 0],  [0, 1]] for addr in range(0, 8)]
        ),
        TestLogic("Select 1", default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 0],  [1, 0]] for addr in range(0, 8)]
        ),
        TestLogic("Inhibit 0", default_inputs, default_outputs,
            body=[[[*BV.int(0, 8), *addr, 1],  [0, 1]] for addr in BV.range(0, 8)]
        ),
        TestLogic("Inhibit 1", default_inputs, default_outputs,
            body=[[[*~BV.int(0, 8), *addr, 1],  [0, 1]] for addr in BV.range(0, 8)]
        )
    ]
