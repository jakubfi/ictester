from binvec import BV
from part import (PackageDIP20, Pin, PinType, ZIFFunc)
from test import TestLogic

class Part74S240(PackageDIP20):
    name = "74S240"
    desc = "Inverting Octal Buffers and Line Drivers With 3-State Outputs"
    pin_cfg = {
        1: Pin("~1G", PinType.IN),
        2: Pin("1A1", PinType.IN),
        3: Pin("~2Y4", PinType.ST3),
        4: Pin("1A2", PinType.IN),
        5: Pin("~2Y3", PinType.ST3),
        6: Pin("1A3", PinType.IN),
        7: Pin("~2Y2", PinType.ST3),
        8: Pin("1A4", PinType.IN),
        9: Pin("~2Y1", PinType.ST3),
        11: Pin("2A1", PinType.IN),
        12: Pin("~1Y4", PinType.ST3),
        13: Pin("2A2", PinType.IN),
        14: Pin("~1Y3", PinType.ST3),
        15: Pin("2A3", PinType.IN),
        16: Pin("~1Y2", PinType.ST3),
        17: Pin("2A4", PinType.IN),
        18: Pin("~1Y1", PinType.ST3),
        19: Pin("~2G", PinType.IN),
    }

    default_inputs = [1,  2, 4, 6, 8,  19,  11, 13, 15, 17]
    default_outputs = [18, 16, 14, 12,  9, 7, 5, 3]

    tests = [
        TestLogic("Outputs enabled", default_inputs, default_outputs,
            body=[
                [[0,  1, 1, 1, 1,  0,  1, 1, 1, 1], [0, 0, 0, 0,  0, 0, 0, 0]],
                [[0,  0, 0, 0, 0,  0,  0, 0, 0, 0], [1, 1, 1, 1,  1, 1, 1, 1]],
            ]
        ),
        TestLogic("Outputs disabled", default_inputs, default_outputs,
            read_delay_us=2,  # with weak pullup, disabled (HiZ) outputs require more time to settle
            body=[
                [[1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [1, 1, 1, 1,  1, 1, 1, 1]],
                [[1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [1, 1, 1, 1,  1, 1, 1, 1]],
            ]
        ),
    ]
