from binvec import BV
from prototypes import (PackageDIP24, Pin, PinType, TestLogic)

class Part74150(PackageDIP24):
    name = "74150"
    desc = "Data selectors/multiplexers"
    pin_cfg = {
        1: Pin("E7", PinType.IN),
        2: Pin("E6", PinType.IN),
        3: Pin("E5", PinType.IN),
        4: Pin("E4", PinType.IN),
        5: Pin("E3", PinType.IN),
        6: Pin("E2", PinType.IN),
        7: Pin("E1", PinType.IN),
        8: Pin("E0", PinType.IN),
        9: Pin("~G", PinType.IN),
        10: Pin("W", PinType.OUT),
        11: Pin("D", PinType.IN),
        13: Pin("C", PinType.IN),
        14: Pin("B", PinType.IN),
        15: Pin("A", PinType.IN),
        16: Pin("E15", PinType.IN),
        17: Pin("E14", PinType.IN),
        18: Pin("E13", PinType.IN),
        19: Pin("E12", PinType.IN),
        20: Pin("E11", PinType.IN),
        21: Pin("E10", PinType.IN),
        22: Pin("E9", PinType.IN),
        23: Pin("E8", PinType.IN),
    }

    default_inputs = [11, 13, 14, 15,  9,  16, 17, 18, 19, 20, 21, 22, 23, 1, 2, 3, 4, 5, 6, 7, 8]
    default_outputs = [10]

    tests = [
        TestLogic("Select 0", default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 0, *~BV.bit(addr, 16)],  [1]] for addr in range(0, 15)]
        ),
        TestLogic("Select 1", default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 0, *BV.bit(addr, 16)],  [0]] for addr in range(0, 15)]
        ),
        TestLogic("Inhibit 0", default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 1, *BV.int(0, 16)],  [1]] for addr in range(0, 15)]
        ),
        TestLogic("Inhibit 1", default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 1, *~BV.int(0, 16)],  [1]] for addr in range(0, 15)]
        ),
    ]
