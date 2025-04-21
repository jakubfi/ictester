from ictester.part import (PackageDIP14_vcc5, Pin, PinType)
from ictester.test import TestLogic

class Part7492(PackageDIP14_vcc5):
    name = "7492"
    desc = "Divide By-Twelve counters"
    pin_cfg = {
        1: Pin("CKB", PinType.IN),
        2: Pin("NC", PinType.NC),
        3: Pin("NC", PinType.NC),
        4: Pin("NC", PinType.NC),
        6: Pin("R0(1)", PinType.IN),
        7: Pin("Ro(2)", PinType.IN),
        8: Pin("QD", PinType.OUT),
        9: Pin("QC", PinType.OUT),
        11: Pin("QB", PinType.OUT),
        12: Pin("QA", PinType.OUT),
        13: Pin("NC", PinType.NC),
        14: Pin("CKA", PinType.IN),
    }

    test_count = TestLogic("Count",
        inputs=[6, 7,  14, 1],
        outputs=[12, 11, 9, 8],
        body=[
            # initial reset
            [['+', '+',  0, 0], [0, 0, 0, 0]],
            # count CKA
            [[0, 0,  '+', 0], [1, 0, 0, 0]],
            [[0, 0,  '+', 0], [0, 0, 0, 0]],  # div 2
            [[0, 0,  '+', 0], [1, 0, 0, 0]],
            # reset bit QA
            [['-', '-',  0, 0], [0, 0, 0, 0]],
            # count CKB
            [[0, 0,  0, '+'], [0, 1, 0, 0]],
            [[0, 0,  0, '+'], [0, 0, 1, 0]],
            [[0, 0,  0, '+'], [0, 0, 0, 1]],
            [[0, 0,  0, '+'], [0, 1, 0, 1]],
            [[0, 0,  0, '+'], [0, 0, 1, 1]],
            [[0, 0,  0, '+'], [0, 0, 0, 0]],  # div 6
            # count again to fill some bits with 1s
            [[0, 0,  '+', 0], [1, 0, 0, 0]],
            [[0, 0,  0, '+'], [1, 1, 0, 0]],
            [[0, 0,  0, '+'], [1, 0, 1, 0]],
            [[0, 0,  0, '+'], [1, 0, 0, 1]],
            [[0, 0,  0, '+'], [1, 1, 0, 1]],
            [[0, 0,  0, '+'], [1, 0, 1, 1]],
            # no reset
            [[0, '+',  0, 0], [1, 0, 1, 1]],
            [['+', 0,  0, 0], [1, 0, 1, 1]],
            # reset bits QC, QD
            [['+', '+',  0, 0], [0, 0, 0, 0]],
            # set bit QB
            [[0, 0,  0, '+'], [0, 1, 0, 0]],
            # reset bit QB
            [['+', '+',  0, 0], [0, 0, 0, 0]],
        ]
    )

    tests = [test_count]
