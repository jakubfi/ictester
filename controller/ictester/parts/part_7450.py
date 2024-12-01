from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

class Part7450(PackageDIP14):
    name = "7450"
    desc = "Dual 2−Wide 2−Input AND/OR Invert Gate (One Gate Expandable)"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("2A", PinType.IN),
        3: Pin("2B", PinType.IN),
        4: Pin("2C", PinType.IN),
        5: Pin("2D", PinType.IN),
        6: Pin("2Y", PinType.OUT),
        8: Pin("1Y", PinType.OUT),
        9: Pin("1C", PinType.IN),
        10: Pin("1D", PinType.IN),
        11: Pin("1X", PinType.NC),
        12: Pin("~1X", PinType.NC),
        13: Pin("1B", PinType.IN),
    }

    missing_tests = "Gate expansion is not tested"

    test_async = TestLogic("Asynchronous operation",
        inputs=[1, 13, 9, 10,  2, 3, 4, 5],
        outputs=[8, 6],
        body=[
            [[*ab1, *cd1, *ab2, *cd2],  [not (ab1.vand() or cd1.vand()), not (ab2.vand() or cd2.vand())]]
            for ab1 in BV.range(0, 2**2)
            for cd1 in BV.range(0, 2**2)
            for ab2 in BV.range(0, 2**2)
            for cd2 in BV.range(0, 2**2)
        ]
    )

    tests = [test_async]
