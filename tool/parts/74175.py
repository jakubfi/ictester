from prototypes import (PackageDIP16, Pin, Test)

class Part74175(PackageDIP16):
    name = "74175"
    desc = "Quad D-type filp-flops"
    pin_cfg = {
        1: Pin("~CLR", Pin.IN),
        2: Pin("1Q", Pin.OUT),
        3: Pin("~1Q", Pin.OUT),
        4: Pin("1D", Pin.IN),
        5: Pin("2D", Pin.IN),
        6: Pin("~2Q", Pin.OUT),
        7: Pin("2Q", Pin.OUT),
        9: Pin("CLK", Pin.IN),
        10: Pin("3Q", Pin.OUT),
        11: Pin("~3Q", Pin.OUT),
        12: Pin("3D", Pin.IN),
        13: Pin("4D", Pin.IN),
        14: Pin("~4Q", Pin.OUT),
        15: Pin("4Q", Pin.OUT),
    }
    test_sync = Test(
        name="Synchronous operation",
        inputs=[1, 9,  4, 5, 12, 13],
        outputs=[2, 3,  7, 6,  10, 11,  15, 14],
        ttype=Test.SEQ,
        body=[
            [[1, '+',  0, 0, 0, 0], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, '+',  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[1, '+',  0, 0, 0, 0], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, '+',  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
        ]
    )
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 9,  4, 5, 12, 13],
        outputs=[2, 3,  7, 6,  10, 11,  15, 14],
        ttype=Test.COMB,
        body=[
            # clear
            [[0, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            # load 1s
            [[1, 1,  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[1, 0,  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            # clear
            [[0, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
        ]
    )
    tests = [test_sync, test_async]
