from ictester.part import (PackageDIP16_vcc5, Pin, PinType)
from ictester.test import TestLogic

class Part7475(PackageDIP16_vcc5):
    name = "7475"
    desc = "4-bit bistable latches"
    pin_cfg = {
        1: Pin("~1Q", PinType.OUT),
        2: Pin("1D", PinType.IN),
        3: Pin("2D", PinType.IN),
        4: Pin("3C,4C", PinType.IN),
        6: Pin("3D", PinType.IN),
        7: Pin("4D", PinType.IN),
        8: Pin("~4Q", PinType.OUT),
        9: Pin("4Q", PinType.OUT),
        10: Pin("3Q", PinType.OUT),
        11: Pin("~3Q", PinType.OUT),
        13: Pin("1C,2C", PinType.IN),
        14: Pin("~2Q", PinType.OUT),
        15: Pin("2Q", PinType.OUT),
        16: Pin("1Q", PinType.OUT),
    }

    test_follow = TestLogic("Follow",
        inputs=[2, 3, 13,  6, 7, 4],
        outputs=[16, 1,  15, 14,  10, 11,  9, 8],
        body=[
            [[0, 0, 1,  0, 0, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[0, 1, 1,  0, 1, 1], [0, 1,  1, 0,  0, 1,  1, 0]],
            [[1, 0, 1,  1, 0, 1], [1, 0,  0, 1,  1, 0,  0, 1]],
            [[1, 1, 1,  1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[1, 1, 0,  1, 1, 0], [1, 0,  1, 0,  1, 0,  1, 0]],
        ]
    )

    test_toggle = TestLogic("Store/No change",
        inputs=[2, 3, 13,  6, 7, 4],
        outputs=[16, 1,  15, 14,  10, 11,  9, 8],
        body=[
            [[0, 0, '+',  0, 0, '+'], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 1,   0,  1, 1,   0], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[0, 1, '+',  0, 1, '+'], [0, 1,  1, 0,  0, 1,  1, 0]],
            [[1, 0,   0,  1, 0,   0], [0, 1,  1, 0,  0, 1,  1, 0]],
            [[1, 0, '+',  1, 0, '+'], [1, 0,  0, 1,  1, 0,  0, 1]],
            [[0, 1,   0,  0, 1,   0], [1, 0,  0, 1,  1, 0,  0, 1]],
            [[1, 1, '+',  1, 1, '+'], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[0, 0,   0,  0, 0,   0], [1, 0,  1, 0,  1, 0,  1, 0]],
        ]
    )

    tests = [test_follow, test_toggle]
