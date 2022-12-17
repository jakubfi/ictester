from prototypes import (PackageDIP14, Pin, Test)

class Part7450(PackageDIP14):
    name = "7450"
    desc = "Dual 2−Wide 2−Input AND/OR Invert Gate (One Gate Expandable)"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("2A", Pin.IN),
        3: Pin("2B", Pin.IN),
        4: Pin("2C", Pin.IN),
        5: Pin("2D", Pin.IN),
        6: Pin("2Y", Pin.OUT),
        8: Pin("1Y", Pin.OUT),
        9: Pin("1C", Pin.IN),
        10: Pin("1D", Pin.IN),
        11: Pin("1X", Pin.NC),
        12: Pin("~1X", Pin.NC),
        13: Pin("1B", Pin.IN),
    }
    missing_tests = "Gate expansion is not tested"
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 13, 9, 10,  2, 3, 4, 5],
        outputs=[8, 6],
        ttype=Test.COMB,
        body=[
            [2 * i, 2 * [not ((i[0] & i[1]) | (i[2] & i[3]))]]
            for i in Test.binary_combinator(4)
        ]
    )
    tests = [test_async]