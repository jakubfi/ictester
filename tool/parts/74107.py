from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74107(PackageDIP14):
    name = "74107"
    desc = "Dual J-K flip-flops with clear"
    pin_cfg = {
        1: Pin("1J", PinType.IN),
        2: Pin("~1Q", PinType.OUT),
        3: Pin("1Q", PinType.OUT),
        4: Pin("1K", PinType.IN),
        5: Pin("2Q", PinType.OUT),
        6: Pin("~2Q", PinType.OUT),
        8: Pin("2J", PinType.IN),
        9: Pin("2CLK", PinType.IN),
        10: Pin("~2CLR", PinType.IN),
        11: Pin("2K", PinType.IN),
        12: Pin("1CLK", PinType.IN),
        13: Pin("~1CLR", PinType.IN),
    }

    test_all = Test("Complete logic", Test.LOGIC,
        inputs=[1, 4, 12, 13,  8, 11, 9, 10],
        outputs=[3, 2,  5, 6],
        body=[
            # reset
            [[1, 1, '-', 0,  1, 1, '-', 0], [0, 1,  0, 1]],
            # J
            [[1, 0, '-', 1,  1, 0, '-', 1], [1, 0,  1, 0]],
            # hold
            [[0, 0, '-', 1,  0, 0, '-', 1], [1, 0,  1, 0]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [0, 1,  0, 1]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [1, 0,  1, 0]],
            # K
            [[0, 1, '-', 1,  0, 1, '-', 1], [0, 1,  0, 1]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [1, 0,  1, 0]],
        ]
    )

    tests = [test_all]
