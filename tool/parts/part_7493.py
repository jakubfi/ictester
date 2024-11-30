from part import (PackageDIP14_vcc5, Pin, PinType)
from test import TestLogic

class Part7493(PackageDIP14_vcc5):
    name = "7493"
    desc = "4-bit binary counter"
    pin_cfg = {
        1: Pin("CKB", PinType.IN),
        2: Pin("R0(1)", PinType.IN),
        3: Pin("R0(2)", PinType.IN),
        4: Pin("NC", PinType.NC),
        6: Pin("NC", PinType.NC),
        7: Pin("NC", PinType.NC),
        8: Pin("QC", PinType.OUT),
        9: Pin("QB", PinType.OUT),
        11: Pin("QD", PinType.OUT),
        12: Pin("QA", PinType.OUT),
        13: Pin("NC", PinType.NC),
        14: Pin("CKA", PinType.IN),
    }

    test_count = TestLogic("Count",
        inputs=[2, 3,  14, 1],
        outputs=[12, 9, 8, 11],
        body=[
            # reset
            [['\\', '\\',  0, 0], [0, 0, 0, 0]],
            # count CKA
            [[0, 0,  '\\', 0], [1, 0, 0, 0]],
            [[0, 0,  '\\', 0], [0, 0, 0, 0]],
            [[0, 0,  '\\', 0], [1, 0, 0, 0]],
            # reset
            [['\\', '\\',  0, 0], [0, 0, 0, 0]],
            # count CKB
            [[0, 0,  0, '\\'], [0, 1, 0, 0]],
            [[0, 0,  0, '\\'], [0, 0, 1, 0]],
            [[0, 0,  0, '\\'], [0, 1, 1, 0]],
            [[0, 0,  0, '\\'], [0, 0, 0, 1]],
            [[0, 0,  0, '\\'], [0, 1, 0, 1]],
            [[0, 0,  0, '\\'], [0, 0, 1, 1]],
            [[0, 0,  0, '\\'], [0, 1, 1, 1]],
            [[0, 0,  0, '\\'], [0, 0, 0, 0]],
            # count CKB again to fill all bits with 1s
            [[0, 0,  0, '\\'], [0, 1, 0, 0]],
            [[0, 0,  0, '\\'], [0, 0, 1, 0]],
            [[0, 0,  0, '\\'], [0, 1, 1, 0]],
            [[0, 0,  0, '\\'], [0, 0, 0, 1]],
            [[0, 0,  0, '\\'], [0, 1, 0, 1]],
            [[0, 0,  0, '\\'], [0, 0, 1, 1]],
            [[0, 0,  0, '\\'], [0, 1, 1, 1]],
            # no reset
            [[0, '\\',  0, 0], [0, 1, 1, 1]],
            [['\\', 0,  0, 0], [0, 1, 1, 1]],
        ]
    )

    tests = [test_count]
