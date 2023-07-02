from binvec import BV
from prototypes import (PackageDIP14, Pin, Test)

class Part74H53(PackageDIP14):
    name = "74H53"
    desc = "Expandable 4-wide, 2-2-3-2 And-Or-Invert gate"
    pin_cfg = {
        1: Pin("A1", Pin.IN),
        2: Pin("B1", Pin.IN),
        3: Pin("B2", Pin.IN),
        4: Pin("C1", Pin.IN),
        5: Pin("C2", Pin.IN),
        6: Pin("C3", Pin.IN),
        8: Pin("~Y", Pin.OUT),
        9: Pin("D1", Pin.IN),
        10: Pin("D2", Pin.IN),
        11: Pin("X", Pin.NC),
        12: Pin("~X", Pin.NC),
        13: Pin("A2", Pin.IN),
    }

    missing_tests = "Gate expansion is not tested"

    test_async = Test("Asynchronous operation", Test.COMB,
        inputs=[1, 13, 2, 3, 4, 5, 6, 9, 10],
        outputs=[8],
        loops=128,
        body=lambda: [
            [[*ab, *cd, *efg, *hi], [~(ab.vand() | cd.vand() | efg.vand() | hi.vand())]]
            for ab in BV.range(0, 4)
            for cd in BV.range(0, 4)
            for efg in BV.range(0, 8)
            for hi in BV.range(0, 4)
        ]
    )

    tests = [test_async]