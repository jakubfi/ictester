from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74148(PackageDIP16):
    name = "74148"
    desc = "8-line to 3-line priority encoder"
    pin_cfg = {
         1: Pin("4", PinType.IN),
         2: Pin("5", PinType.IN),
         3: Pin("6", PinType.IN),
         4: Pin("7", PinType.IN),
         5: Pin("EI", PinType.IN),
         6: Pin("A2", PinType.OUT),
         7: Pin("A1", PinType.OUT),
         9: Pin("A0", PinType.OUT),
        10: Pin("0", PinType.IN),
        11: Pin("1", PinType.IN),
        12: Pin("2", PinType.IN),
        13: Pin("3", PinType.IN),
        14: Pin("GS", PinType.OUT),
        15: Pin("E0", PinType.OUT),
    }

    test_all = TestLogic("Complete logic",
        inputs=[5,  10, 11, 12, 13, 1, 2, 3, 4],
        outputs=[6, 7, 9, 14, 15],
        body=[
            [[1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1,  1, 1]],
            [[1,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,  1, 1]],

            [[0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,  1, 0]],

            [[0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0,  0, 1]],
            [[0,  0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1,  0, 1]],
            [[0,  0, 0, 0, 0, 0, 0, 1, 1], [0, 1, 0,  0, 1]],
            [[0,  0, 0, 0, 0, 0, 1, 1, 1], [0, 1, 1,  0, 1]],
            [[0,  0, 0, 0, 0, 1, 1, 1, 1], [1, 0, 0,  0, 1]],
            [[0,  0, 0, 0, 1, 1, 1, 1, 1], [1, 0, 1,  0, 1]],
            [[0,  0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 0,  0, 1]],
            [[0,  0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,  0, 1]],

            [[0,  1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0,  0, 1]],
            [[0,  1, 1, 1, 1, 1, 1, 0, 1], [0, 0, 1,  0, 1]],
            [[0,  1, 1, 1, 1, 1, 0, 1, 1], [0, 1, 0,  0, 1]],
            [[0,  1, 1, 1, 1, 0, 1, 1, 1], [0, 1, 1,  0, 1]],
            [[0,  1, 1, 1, 0, 1, 1, 1, 1], [1, 0, 0,  0, 1]],
            [[0,  1, 1, 0, 1, 1, 1, 1, 1], [1, 0, 1,  0, 1]],
            [[0,  1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 0,  0, 1]],
            [[0,  0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,  0, 1]],

        ]
    )

    tests = [test_all]
