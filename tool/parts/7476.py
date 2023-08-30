from prototypes import (PackageDIP16_vcc5_gnd13, Pin, PinType, Test)

class Part7476(PackageDIP16_vcc5_gnd13):
    name = "7476"
    desc = "Dual J−K Flip−Flop with Preset and Clear"
    pin_cfg = {
        1: Pin("1CLK", PinType.IN),
        2: Pin("~1PRE", PinType.IN),
        3: Pin("~1CLR", PinType.IN),
        4: Pin("1J", PinType.IN),
        6: Pin("2CLK", PinType.IN),
        7: Pin("~2PRE", PinType.IN),
        8: Pin("~2CLR", PinType.IN),
        9: Pin("2J", PinType.IN),
        10: Pin("~2Q", PinType.OUT),
        11: Pin("2Q", PinType.OUT),
        12: Pin("2K", PinType.IN),
        14: Pin("~1Q", PinType.OUT),
        15: Pin("1Q", PinType.OUT),
        16: Pin("1K", PinType.IN),
    }

    test_all = Test("Sync/Async operation", Test.SEQ,
        inputs=[2, 3, 1, 4, 16,  7, 8, 6, 9, 12],
        outputs=[15, 14,  11, 10],
        body=[
            # load 1
            [[1, 1, '-', 1, 0,  1, 1, '-', 1, 0], [1, 0,  1, 0]],
            # keep
            [[1, 1, '-', 0, 0,  1, 1, '-', 0, 0], [1, 0,  1, 0]],
            # load 0
            [[1, 1, '-', 0, 1,  1, 1, '-', 0, 1], [0, 1,  0, 1]],
            # keep
            [[1, 1, '-', 0, 0,  1, 1, '-', 0, 0], [0, 1,  0, 1]],
            # toggle
            [[1, 1, '-', 1, 1,  1, 1, '-', 1, 1], [1, 0,  1, 0]],
            # keep
            [[1, 1, '-', 0, 0,  1, 1, '-', 0, 0], [1, 0,  1, 0]],

            # clear with J=0, K=0
            [[1, 1, '-', 1, 0,  1, 1, '-', 1, 0], [1, 0,  1, 0]],
            [[1, 0, '-', 0, 0,  1, 0, '-', 0, 0], [0, 1,  0, 1]],
            # clear with J=1, K=0
            [[1, 1, '-', 1, 0,  1, 1, '-', 1, 0], [1, 0,  1, 0]],
            [[1, 0, '-', 1, 0,  1, 0, '-', 1, 0], [0, 1,  0, 1]],
            # clear with J=0, K=1
            [[1, 1, '-', 1, 0,  1, 1, '-', 1, 0], [1, 0,  1, 0]],
            [[1, 0, '-', 0, 1,  1, 0, '-', 0, 1], [0, 1,  0, 1]],
            # clear with J=1, K=1
            [[1, 1, '-', 1, 0,  1, 1, '-', 1, 0], [1, 0,  1, 0]],
            [[1, 0, '-', 1, 1,  1, 0, '-', 1, 1], [0, 1,  0, 1]],

            # preset with J=0, K=0
            [[1, 1, '-', 0, 1,  1, 1, '-', 0, 1], [0, 1,  0, 1]],
            [[0, 1, '-', 0, 0,  0, 1, '-', 0, 0], [1, 0,  1, 0]],
            # preset with J=1, K=0
            [[1, 1, '-', 0, 1,  1, 1, '-', 0, 1], [0, 1,  0, 1]],
            [[0, 1, '-', 1, 0,  0, 1, '-', 1, 0], [1, 0,  1, 0]],
            # preset with J=0, K=1
            [[1, 1, '-', 0, 1,  1, 1, '-', 0, 1], [0, 1,  0, 1]],
            [[0, 1, '-', 0, 1,  0, 1, '-', 0, 1], [1, 0,  1, 0]],
            # preset with J=1, K=1
            [[1, 1, '-', 0, 1,  1, 1, '-', 0, 1], [0, 1,  0, 1]],
            [[0, 1, '-', 1, 1,  0, 1, '-', 1, 1], [1, 0,  1, 0]],
        ]
    )

    tests = [test_all]
