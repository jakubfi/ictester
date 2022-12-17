from prototypes import (PackageDIP14, Pin, Test)

class Part7452(PackageDIP14):
    name = "7452"
    desc = "AND-OR Gate (Expandable)"
    pin_cfg = {
        1: Pin("A", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("C", Pin.IN),
        4: Pin("D", Pin.IN),
        5: Pin("E", Pin.IN),
        6: Pin("NC", Pin.NC),
        8: Pin("Y", Pin.OUT),
        9: Pin("X", Pin.NC),
        10: Pin("F", Pin.IN),
        11: Pin("G", Pin.IN),
        12: Pin("H", Pin.IN),
        13: Pin("I", Pin.IN),
    }
    missing_tests = "Gate expansion is not tested"
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 2,  3, 4, 5,  10, 11,  12, 13],
        outputs=[8],
        ttype=Test.COMB,
        loops=128,
        body=[
            [i, [(i[0] & i[1]) | (i[2] & i[3] & i[4]) | (i[5] & i[6]) | (i[7] & i[8])]]
            for i in Test.binary_combinator(9)
        ]
    )
    tests = [test_async]