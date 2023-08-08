from prototypes import (PackageDIP14_vcc4, Pin, PinType, Test)

class Part7473(PackageDIP14_vcc4):
    name = "7473"
    desc = "Dual J−K Flip−Flop with Clear"
    pin_cfg = {
        1: Pin("1CLK", PinType.IN),
        2: Pin("~1CLR", PinType.IN),
        3: Pin("1K", PinType.IN),
        5: Pin("2CLK", PinType.IN),
        6: Pin("~2CLR", PinType.IN),
        7: Pin("2J", PinType.IN),
        8: Pin("~2Q", PinType.OUT),
        9: Pin("2Q", PinType.OUT),
        10: Pin("2K", PinType.IN),
        12: Pin("1Q", PinType.OUT),
        13: Pin("~1Q", PinType.OUT),
        14: Pin("1J", PinType.IN),
    }

    test_all = Test("Sync/Async operation", Test.SEQ,
        inputs=[14, 3, 2, 1,  7, 10, 6, 5],
        outputs=[12, 13, 9, 8],
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
