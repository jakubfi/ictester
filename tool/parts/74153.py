from prototypes import (PackageDIP16, Pin, Test)

class Part74153(PackageDIP16):
    name = "74153"
    desc = "Dual 4-line to 1-line data selectors/multiplexers"
    pin_cfg = {
        1: Pin("~1G", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("1C3", Pin.IN),
        4: Pin("1C2", Pin.IN),
        5: Pin("1C1", Pin.IN),
        6: Pin("1C0", Pin.IN),
        7: Pin("1Y", Pin.OUT),
        9: Pin("2Y", Pin.OUT),
        10: Pin("2C0", Pin.IN),
        11: Pin("2C1", Pin.IN),
        12: Pin("2C2", Pin.IN),
        13: Pin("2C3", Pin.IN),
        14: Pin("A", Pin.IN),
        15: Pin("~2G", Pin.IN),
    }
    test_all = Test(
        name="Complete logic",
        inputs=[2, 14, 1, 3, 4, 5, 6, 15, 13, 12, 11, 10],
        outputs=[7, 9],
        ttype=Test.COMB,
        body=[
            # output is always "0" when G is high
            [[0, 0,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[0, 1,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[1, 0,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[1, 1,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[0, 0,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[0, 1,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[1, 0,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[1, 1,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],

            # selection if G is low
            [[0, 0,  0,  1, 1, 1, 0,  0,  1, 1, 1, 0], [0, 0]],
            [[0, 1,  0,  1, 1, 0, 1,  0,  1, 1, 0, 1], [0, 0]],
            [[1, 0,  0,  1, 0, 1, 1,  0,  1, 0, 1, 1], [0, 0]],
            [[1, 1,  0,  0, 1, 1, 1,  0,  0, 1, 1, 1], [0, 0]],

            [[0, 0,  0,  0, 0, 0, 1,  0,  0, 0, 0, 1], [1, 1]],
            [[0, 1,  0,  0, 0, 1, 0,  0,  0, 0, 1, 0], [1, 1]],
            [[1, 0,  0,  0, 1, 0, 0,  0,  0, 1, 0, 0], [1, 1]],
            [[1, 1,  0,  1, 0, 0, 0,  0,  1, 0, 0, 0], [1, 1]],
        ]
    )
    tests = [test_all]
