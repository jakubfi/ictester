from prototypes import (PackageDIP16, Pin, PinType, Test)

class Part74175(PackageDIP16):
    name = "74175"
    desc = "Quad D-type filp-flops"
    pin_cfg = {
        1: Pin("~CLR", PinType.IN),
        2: Pin("1Q", PinType.OUT),
        3: Pin("~1Q", PinType.OUT),
        4: Pin("1D", PinType.IN),
        5: Pin("2D", PinType.IN),
        6: Pin("~2Q", PinType.OUT),
        7: Pin("2Q", PinType.OUT),
        9: Pin("CLK", PinType.IN),
        10: Pin("3Q", PinType.OUT),
        11: Pin("~3Q", PinType.OUT),
        12: Pin("3D", PinType.IN),
        13: Pin("4D", PinType.IN),
        14: Pin("~4Q", PinType.OUT),
        15: Pin("4Q", PinType.OUT),
    }

    default_inputs = [1, 9,  4, 5, 12, 13]
    default_outputs = [2, 3,  7, 6,  10, 11,  15, 14]

    test_sync = Test("Synchronous operation", Test.LOGIC, default_inputs, default_outputs,
        body=[
            [[1, '/',  0, 0, 0, 0], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, '/',  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[1, '/',  0, 0, 0, 0], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, '/',  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
        ]
    )
    test_async = Test("Asynchronous operation", Test.LOGIC, default_inputs, default_outputs,
        body=[
            # clear
            [[0, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            # load 1s
            [[1, 1,  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[1, 0,  1, 1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            # clear
            [[0, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 0,  1, 1, 1, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
        ]
    )

    tests = [test_sync, test_async]
