from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part74194(PackageDIP16):
    name = "74194"
    desc = "4-bit bidirectional universal shift register"
    pin_cfg = {
        1: Pin("~CLR", PinType.IN),
        2: Pin("SR_SER", PinType.IN),
        3: Pin("A", PinType.IN),
        4: Pin("B", PinType.IN),
        5: Pin("C", PinType.IN),
        6: Pin("D", PinType.IN),
        7: Pin("SL_SER", PinType.IN),
        9: Pin("S0", PinType.IN),
        10: Pin("S1", PinType.IN),
        11: Pin("CLK", PinType.IN),
        12: Pin("QD", PinType.OUT),
        13: Pin("QC", PinType.OUT),
        14: Pin("QB", PinType.OUT),
        15: Pin("QA", PinType.OUT),
    }

    default_inputs = [1,  10, 9,  11,  7, 2,  3, 4, 5, 6]
    default_outputs = [15, 14, 13, 12]

    test_load = TestLogic("Load", default_inputs, default_outputs,
        body=[
            # load 1's
            [[1,  1, 1,  '/',  0, 0,  1, 1, 1, 1], [1, 1, 1, 1]],
            # output current
            [[1,  0, 0,  '/',  0, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            # load 0's
            [[1,  1, 1,  '/',  1, 1,  0, 0, 0, 0], [0, 0, 0, 0]],
            # output current
            [[1,  0, 0,  '/',  1, 1,  1, 1, 1, 1], [0, 0, 0, 0]],

        ]
    )
    test_shright = TestLogic("Shift right", default_inputs, default_outputs,
        body=[
            # shift right, insert 1's
            [[1,  0, 1,  '/',  0, 1,  0, 0, 0, 0], [1, 0, 0, 0]],
            [[1,  0, 1,  '/',  0, 1,  0, 0, 0, 0], [1, 1, 0, 0]],
            [[1,  0, 1,  '/',  0, 1,  0, 0, 0, 0], [1, 1, 1, 0]],
            [[1,  0, 1,  '/',  0, 1,  0, 0, 0, 0], [1, 1, 1, 1]],
            # shift right, insert 0's
            [[1,  0, 1,  '/',  1, 0,  1, 1, 1, 1], [0, 1, 1, 1]],
            [[1,  0, 1,  '/',  1, 0,  1, 1, 1, 1], [0, 0, 1, 1]],
            [[1,  0, 1,  '/',  1, 0,  1, 1, 1, 1], [0, 0, 0, 1]],
            [[1,  0, 1,  '/',  1, 0,  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )
    test_shleft = TestLogic("Shift left", default_inputs, default_outputs,
        body=[
            # shift left, insert 1's
            [[1,  1, 0,  '/',  1, 0,  0, 0, 0, 0], [0, 0, 0, 1]],
            [[1,  1, 0,  '/',  1, 0,  0, 0, 0, 0], [0, 0, 1, 1]],
            [[1,  1, 0,  '/',  1, 0,  0, 0, 0, 0], [0, 1, 1, 1]],
            [[1,  1, 0,  '/',  1, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            # shift left, insert 0's
            [[1,  1, 0,  '/',  0, 1,  1, 1, 1, 1], [1, 1, 1, 0]],
            [[1,  1, 0,  '/',  0, 1,  1, 1, 1, 1], [1, 1, 0, 0]],
            [[1,  1, 0,  '/',  0, 1,  1, 1, 1, 1], [1, 0, 0, 0]],
            [[1,  1, 0,  '/',  0, 1,  1, 1, 1, 1], [0, 0, 0, 0]],

        ]
    )
    test_clear = TestLogic("Clear", default_inputs, default_outputs,
        body=[
            # load 1's
            [[1,  1, 1,  '/',  0, 0,  1, 1, 1, 1], [1, 1, 1, 1]],
            # clear
            [[0,  1, 1,  '/',  1, 1,  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )

    tests = [test_load, test_shright, test_shleft, test_clear]
