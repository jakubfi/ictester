from prototypes import (PackageDIP16, Pin, Test)

class Part74174(PackageDIP16):
    name = "74174"
    desc = "Hex D-type filp-flops with clear"
    pin_cfg = {
        1: Pin("~CLR", Pin.IN),
        2: Pin("1Q", Pin.OUT),
        3: Pin("1D", Pin.IN),
        4: Pin("2D", Pin.IN),
        5: Pin("2Q", Pin.OUT),
        6: Pin("3D", Pin.IN),
        7: Pin("3Q", Pin.OUT),
        9: Pin("CLK", Pin.IN),
        10: Pin("4Q", Pin.OUT),
        11: Pin("4D", Pin.IN),
        12: Pin("5Q", Pin.OUT),
        13: Pin("5D", Pin.IN),
        14: Pin("6D", Pin.IN),
        15: Pin("6Q", Pin.OUT),
    }
    test_sync = Test(
        name="Synchronous operation",
        inputs=[1, 9,  3, 4, 6, 11, 13, 14],
        outputs=[2, 5, 7, 10, 12, 15],
        ttype=Test.SEQ,
        body=[
            [[1, '+',  0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            [[1, '+',  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            [[1, '+',  0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            [[1, '+',  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
        ]
    )
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 9,  3, 4, 6, 11, 13, 14],
        outputs=[2, 5, 7, 10, 12, 15],
        ttype=Test.COMB,
        body=[
            # clear
            [[0, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            # load 1s
            [[1, 1,  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            # clear
            [[0, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
        ]
    )
    tests = [test_sync, test_async]

