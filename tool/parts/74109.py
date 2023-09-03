from prototypes import (PackageDIP16, Pin, PinType, Test)

class Part74109(PackageDIP16):
    name = "74109"
    desc = "Dual J-K positive edge triggered flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("~1CLR", PinType.IN),
        2: Pin("1J", PinType.IN),
        3: Pin("~1K", PinType.IN),
        4: Pin("1CLK", PinType.IN),
        5: Pin("~1PRE", PinType.IN),
        6: Pin("1Q", PinType.OUT),
        7: Pin("~1Q", PinType.OUT),
        9: Pin("~2Q", PinType.OUT),
        10: Pin("2Q", PinType.OUT),
        11: Pin("~2PRE", PinType.IN),
        12: Pin("2CLK", PinType.IN),
        13: Pin("~2K", PinType.IN),
        14: Pin("2J", PinType.IN),
        15: Pin("~2CLR", PinType.IN),
    }

    test_all = Test("Complete logic", Test.LOGIC,
        inputs=[4, 5, 1, 2, 3,  12, 11, 15, 14, 13],
        outputs=[6, 7,  10, 9],
        body=[
            # reset
            [[0, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],
            # preset
            [[0, 0, 1, 0, 0,  0, 0, 1, 0, 0], [1, 0,  1, 0]],
            # reset
            [[0, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],

            # J
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [0, 1,  0, 1]],
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [1, 0,  1, 0]],
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [1, 0,  1, 0]],

            # K
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [1, 0,  1, 0]],
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [0, 1,  0, 1]],

            # hold
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [0, 1,  0, 1]],
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [0, 1,  0, 1]],

            # toggle
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [0, 1,  0, 1]],
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [1, 0,  1, 0]],
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [1, 0,  1, 0]],

        ]
    )

    tests = [test_all]
