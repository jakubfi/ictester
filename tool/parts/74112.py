from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part74112(PackageDIP16):
    name = "74112"
    desc = "Dual J-K negative edge triggered flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("1CLK", PinType.IN),
        2: Pin("1K", PinType.IN),
        3: Pin("1J", PinType.IN),
        4: Pin("~1PRE", PinType.IN),
        5: Pin("1Q", PinType.OUT),
        6: Pin("~1Q", PinType.OUT),
        7: Pin("~2Q", PinType.OUT),
        9: Pin("2Q", PinType.OUT),
        10: Pin("~2PRE", PinType.IN),
        11: Pin("2J", PinType.IN),
        12: Pin("2K", PinType.IN),
        13: Pin("2CLK", PinType.IN),
        14: Pin("~2CLR", PinType.IN),
        15: Pin("~1CLR", PinType.IN),
    }

    test_all = TestLogic("Complete logic",
        inputs=[1, 4, 15, 3, 2,  13, 10, 14, 11, 12],
        outputs=[5, 6,  9, 7],
        body=[
            # reset
            [[1, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],
            # preset
            [[1, 0, 1, 0, 0,  0, 0, 1, 0, 0], [1, 0,  1, 0]],
            # reset
            [[1, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],

            # J
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [1, 0,  1, 0]],
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [1, 0,  1, 0]],

            # K
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [1, 0,  1, 0]],
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [0, 1,  0, 1]],

            # hold
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],

            # toggle
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [1, 0,  1, 0]],
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [1, 0,  1, 0]],

        ]
    )

    tests = [test_all]
