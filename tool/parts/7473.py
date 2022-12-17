from prototypes import (PackageDIP14_vcc4, Pin, Test)

class Part7473(PackageDIP14_vcc4):
    name = "7473"
    desc = "Dual J−K Flip−Flop with Clear"
    pin_cfg = {
        1: Pin("1CLK", Pin.IN),
        2: Pin("~1CLR", Pin.IN),
        3: Pin("1K", Pin.IN),
        5: Pin("2CLK", Pin.IN),
        6: Pin("~2CLR", Pin.IN),
        7: Pin("2J", Pin.IN),
        8: Pin("~2Q", Pin.OUT),
        9: Pin("2Q", Pin.OUT),
        10: Pin("2K", Pin.IN),
        12: Pin("1Q", Pin.OUT),
        13: Pin("~1Q", Pin.OUT),
        14: Pin("1J", Pin.IN),
    }
    test_all = Test(
        name="Sync/Async operation",
        inputs=[14, 3, 2, 1,  7, 10, 6, 5],
        outputs=[12, 13, 9, 8],
        ttype=Test.SEQ,
        body=[
            # load 1
            [[1, 0, 1, '-',  1, 0, 1, '-'], [1, 0,  1, 0]],
            # keep
            [[0, 0, 1, '-',  0, 0, 1, '-'], [1, 0,  1, 0]],
            # load 0
            [[0, 1, 1, '-',  0, 1, 1, '-'], [0, 1,  0, 1]],
            # keep
            [[0, 0, 1, '-',  0, 0, 1, '-'], [0, 1,  0, 1]],
            # toggle
            [[1, 1, 1, '-',  1, 1, 1, '-'], [1, 0,  1, 0]],
            # keep
            [[0, 0, 1, '-',  0, 0, 1, '-'], [1, 0,  1, 0]],

            # clear with J=0, K=0
            [[1, 0, 1, '-',  1, 0, 1, '-'], [1, 0,  1, 0]],
            [[0, 0, 0, '-',  0, 0, 0, '-'], [0, 1,  0, 1]],
            # clear with J=1, K=0
            [[1, 0, 1, '-',  1, 0, 1, '-'], [1, 0,  1, 0]],
            [[1, 0, 0, '-',  1, 0, 0, '-'], [0, 1,  0, 1]],
            # clear with J=0, K=1
            [[1, 0, 1, '-',  1, 0, 1, '-'], [1, 0,  1, 0]],
            [[0, 1, 0, '-',  1, 0, 0, '-'], [0, 1,  0, 1]],
            # clear with J=1, K=1
            [[1, 0, 1, '-',  1, 0, 1, '-'], [1, 0,  1, 0]],
            [[1, 1, 0, '-',  1, 0, 0, '-'], [0, 1,  0, 1]],
        ]
    )
    tests = [test_all]
