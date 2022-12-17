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
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 13, 2, 3, 4, 5, 6, 9, 10],
        outputs=[8],
        ttype=Test.COMB,
        loops=128,
        body=[
            [i, [not ((i[0] & i[1]) | (i[2] & i[3]) | (i[4] & i[5] & i[6]) | (i[7] & i[8]))]]
            for i in Test.binary_combinator(9)
        ]
    )
    tests = [test_async]