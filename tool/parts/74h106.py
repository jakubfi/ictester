from prototypes import (PackageDIP16_vcc5_gnd13, Pin, Test)

class Part74H106(PackageDIP16_vcc5_gnd13):
    name = "74H106"
    desc = "Dual J-K flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("1CLK", Pin.IN),
        2: Pin("~1PRE", Pin.IN),
        3: Pin("~1CLR", Pin.IN),
        4: Pin("1J", Pin.IN),
        6: Pin("2CLK", Pin.IN),
        7: Pin("~2PRE", Pin.IN),
        8: Pin("~2CLR", Pin.IN),
        9: Pin("2J", Pin.IN),
        10: Pin("~2Q", Pin.OUT),
        11: Pin("2Q", Pin.OUT),
        12: Pin("2K", Pin.IN),
        14: Pin("~1Q", Pin.OUT),
        15: Pin("1Q", Pin.OUT),
        16: Pin("1K", Pin.IN),
    }

    test_all = Test("Complete logic", Test.COMB,
        inputs=[1, 2, 3, 4, 16,  6, 7, 8, 9, 12],
        outputs=[15, 14,  11, 10],
        body=[
            # reset
            [[0, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],
            # preset
            [[0, 0, 1, 0, 0,  0, 0, 1, 0, 0], [1, 0,  1, 0]],
            # reset
            [[0, 1, 0, 0, 0,  0, 1, 0, 0, 0], [0, 1,  0, 1]],

            # J
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [0, 1,  0, 1]],
            [[1, 1, 1, 1, 0,  1, 1, 1, 1, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 0,  0, 1, 1, 1, 0], [1, 0,  1, 0]],

            # K
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [1, 0,  1, 0]],
            [[1, 1, 1, 0, 1,  1, 1, 1, 0, 1], [1, 0,  1, 0]],
            [[0, 1, 1, 0, 1,  0, 1, 1, 0, 1], [0, 1,  0, 1]],

            # hold
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 1, 1, 0, 0,  1, 1, 1, 0, 0], [0, 1,  0, 1]],
            [[0, 1, 1, 0, 0,  0, 1, 1, 0, 0], [0, 1,  0, 1]],

            # toggle
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [0, 1,  0, 1]],
            [[1, 1, 1, 1, 1,  1, 1, 1, 1, 1], [0, 1,  0, 1]],
            [[0, 1, 1, 1, 1,  0, 1, 1, 1, 1], [1, 0,  1, 0]],
        ]
    )

    tests = [test_all]
