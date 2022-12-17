from prototypes import (PackageDIP14, Pin, Test)

class Part7474(PackageDIP14):
    name = "7474"
    desc = "Dual D-type positive-edge-triggered flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("~1CLR", Pin.IN),
        2: Pin("1D", Pin.IN),
        3: Pin("1CLK", Pin.IN),
        4: Pin("~1PRE", Pin.IN),
        5: Pin("1Q", Pin.OUT),
        6: Pin("~1Q", Pin.OUT),
        8: Pin("~2Q", Pin.OUT),
        9: Pin("2Q", Pin.OUT),
        10: Pin("~2PRE", Pin.IN),
        11: Pin("2CLK", Pin.IN),
        12: Pin("2D", Pin.IN),
        13: Pin("~2CLR", Pin.IN),
    }
    test_sync = Test(
        name="Synchronous operation",
        inputs=[1, 4, 2, 3, 13, 10, 12, 11],
        outputs=[5, 6, 9, 8],
        ttype=Test.SEQ,
        body=[
            [[1, 1, 0, '+',  1, 1, 0, '+'], [0, 1,  0, 1]],
            [[1, 1, 1, '+',  1, 1, 1, '+'], [1, 0,  1, 0]],
        ]
    )
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 4, 2, 3, 13, 10, 12, 11],
        outputs=[5, 6, 9, 8],
        ttype=Test.COMB,
        body=[
            [[0, 1, 0, 0,  0, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 0, 0, 0,  1, 0, 0, 0], [1, 0,  1, 0]],
        ]
    )
    tests = [test_sync, test_async]
