from prototypes import (PackageDIP16_vcc5_gnd13, Pin, PinType, Test)

class Part74H106(PackageDIP16_vcc5_gnd13):
    name = "74H106"
    desc = "Dual J-K flip-flops with preset and clear"
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

    test_all = Test("Complete logic", Test.LOGIC,
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
