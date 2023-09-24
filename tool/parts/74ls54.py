from binvec import BV
from part import (PackageDIP14, Pin, PinType)
from test import TestLogic

class Part74LS54(PackageDIP14):
    name = "74LS54"
    desc = "4-wide And-Or-Invert gate"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("C", PinType.IN),
        4: Pin("D", PinType.IN),
        5: Pin("E", PinType.IN),
        6: Pin("Y", PinType.OUT),
        8: Pin("NC", PinType.NC),
        9: Pin("F", PinType.IN),
        10: Pin("G", PinType.IN),
        11: Pin("H", PinType.IN),
        12: Pin("I", PinType.IN),
        13: Pin("J", PinType.IN),
    }

    test_async = TestLogic("Asynchronous operation",
        inputs=[1, 2,  3, 4, 5,  9, 10, 11,  12, 13],
        outputs=[6],
        loops=256,
        body=lambda: [
            [[*ab, *cde, *fgh, *ij],  [not (ab.vand() or cde.vand() or fgh.vand() or ij.vand())]]
            for ab in BV.range(0, 4)
            for cde in BV.range(0, 8)
            for fgh in BV.range(0, 8)
            for ij in BV.range(0, 4)
        ]
    )

    tests = [test_async]
