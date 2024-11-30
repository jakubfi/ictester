from binvec import BV
from part import (PackageDIP14, Pin, PinType)
from test import TestLogic

class Part74H52(PackageDIP14):
    name = "74H52"
    desc = "AND-OR Gate (Expandable)"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("C", PinType.IN),
        4: Pin("D", PinType.IN),
        5: Pin("E", PinType.IN),
        6: Pin("NC", PinType.NC),
        8: Pin("Y", PinType.OUT),
        9: Pin("X", PinType.NC),
        10: Pin("F", PinType.IN),
        11: Pin("G", PinType.IN),
        12: Pin("H", PinType.IN),
        13: Pin("I", PinType.IN),
    }

    missing_tests = "Gate expansion is not tested"

    test_async = TestLogic("Asynchronous operation",
        inputs=[1, 2,  3, 4, 5,  10, 11,  12, 13],
        outputs=[8],
        loops=128,
        body=lambda: [
            [[*ab, *cde, *fg, *hi], [ab.vand() or cde.vand() or fg.vand() or hi.vand()]]
            for ab in BV.range(0, 2**2)
            for cde in BV.range(0, 2**3)
            for fg in BV.range(0, 2**2)
            for hi in BV.range(0, 2**2)
        ]
    )

    tests = [test_async]
