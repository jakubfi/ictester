from prototypes import (PackageDIP16, Pin, Test)

class Part74112(PackageDIP16):
    name = "74112"
    desc = "Dual J-K negative edge triggered flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("1CLK", Pin.IN),
        2: Pin("1K", Pin.IN),
        3: Pin("1J", Pin.IN),
        4: Pin("~1PRE", Pin.IN),
        5: Pin("1Q", Pin.OUT),
        6: Pin("~1Q", Pin.OUT),
        7: Pin("~2Q", Pin.OUT),
        9: Pin("2Q", Pin.OUT),
        10: Pin("~2PRE", Pin.IN),
        11: Pin("2J", Pin.IN),
        12: Pin("2K", Pin.IN),
        13: Pin("2CLK", Pin.IN),
        14: Pin("~2CLR", Pin.IN),
        15: Pin("~1CLR", Pin.IN),
    }

    test_all = Test("Complete logic", Test.COMB,
        inputs=[1, 4, 15, 3, 2,  13, 10, 14, 11, 12],
        outputs=[5, 6,  9, 7],
        body=[
            # reset
            [[1, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],
            # preset
            [[1, 0, 1, 0, 0,  0, 0, 1, 0, 0], [1, 0,  1, 0]],
            # reset
            [[1, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],

            # J
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [1, 0,  1, 0]],
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [1, 0,  1, 0]],

            # K
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [1, 0,  1, 0]],
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [0, 1,  0, 1]],

            # hold
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],

            # toggle
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [1, 0,  1, 0]],
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [1, 0,  1, 0]],

        ]
    )

    tests = [test_all]
