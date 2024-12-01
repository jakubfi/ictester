from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part7485(PackageDIP16):
    name = "7485"
    desc = "4-bit magnitude comparator"
    pin_cfg = {
        1: Pin("B3", PinType.IN),
        2: Pin("A<Bin", PinType.IN),
        3: Pin("A=Bin", PinType.IN),
        4: Pin("A>Bin", PinType.IN),
        5: Pin("A>Bout", PinType.OUT),
        6: Pin("A=Bout", PinType.OUT),
        7: Pin("A<Bout", PinType.OUT),
        9: Pin("B0", PinType.IN),
        10: Pin("A0", PinType.IN),
        11: Pin("B1", PinType.IN),
        12: Pin("A1", PinType.IN),
        13: Pin("A2", PinType.IN),
        14: Pin("B2", PinType.IN),
        15: Pin("A3", PinType.IN),
    }

    test_all_0 = TestLogic("Full logic (A=B = 0)",
        inputs=[2, 3, 4,  15, 13, 12, 10,  1, 14, 11, 9],
        outputs=[7, 6, 5],
        loops=256,
        body=lambda: [
            [[ls, eq, gt, *a, *b],
            [
                (a < b) or ((a == b) and not gt and not eq),
                (a == b) and eq,
                (a > b) or ((a == b) and not ls and not eq)
            ]]
            for a in BV.range(0, 2**4)
            for b in BV.range(0, 2**4)
            for ls in [0, 1]
            for eq in [0]
            for gt in [0, 1]
        ]
    )

    test_all_1 = TestLogic("Full logic (A=B = 1)",
        inputs=[2, 3, 4,  15, 13, 12, 10,  1, 14, 11, 9],
        outputs=[7, 6, 5],
        loops=256,
        body=lambda: [
            [[ls, eq, gt, *a, *b],
            [
                (a < b) or ((a == b) and not gt and not eq),
                (a == b) and eq,
                (a > b) or ((a == b) and not ls and not eq)
            ]]
            for a in BV.range(0, 2**4)
            for b in BV.range(0, 2**4)
            for ls in [0, 1]
            for eq in [1]
            for gt in [0, 1]
        ]
    )

    # cannot fit both tests in tester memory, merge when more memory available
    tests = [test_all_0, test_all_1]
