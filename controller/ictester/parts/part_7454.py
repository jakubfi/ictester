from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

class Part7454(PackageDIP14):
    name = "7454"
    desc = "4-wide And-Or-Invert gate"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("C", PinType.IN),
        3: Pin("D", PinType.IN),
        4: Pin("E", PinType.IN),
        5: Pin("F", PinType.IN),
        6: Pin("NC", PinType.NC),
        8: Pin("Y", PinType.OUT),
        9: Pin("G", PinType.IN),
        10: Pin("H", PinType.IN),
        11: Pin("NC", PinType.NC),
        12: Pin("NC", PinType.NC),
        13: Pin("B", PinType.IN),
    }

    test_async = TestLogic("Asynchronous operation",
        inputs=[1, 13, 2, 3, 4, 5, 9, 10],
        outputs=[8],
        body=lambda: [
            [
                [*ab, *cd, *ef, *gh],
                [not (ab.vand() or cd.vand() or ef.vand() or gh.vand())]
            ]
            for ab in BV.range(0, 2**2)
            for cd in BV.range(0, 2**2)
            for ef in BV.range(0, 2**2)
            for gh in BV.range(0, 2**2)
        ]
    )

    tests = [test_async]
