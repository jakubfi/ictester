from prototypes import (PackageDIP16, Pin, PinType, TestLogic)

class Part74174(PackageDIP16):
    name = "74174"
    desc = "Hex D-type filp-flops with clear"
    pin_cfg = {
        1: Pin("~CLR", PinType.IN),
        2: Pin("1Q", PinType.OUT),
        3: Pin("1D", PinType.IN),
        4: Pin("2D", PinType.IN),
        5: Pin("2Q", PinType.OUT),
        6: Pin("3D", PinType.IN),
        7: Pin("3Q", PinType.OUT),
        9: Pin("CLK", PinType.IN),
        10: Pin("4Q", PinType.OUT),
        11: Pin("4D", PinType.IN),
        12: Pin("5Q", PinType.OUT),
        13: Pin("5D", PinType.IN),
        14: Pin("6D", PinType.IN),
        15: Pin("6Q", PinType.OUT),
    }

    default_inputs = [1, 9,  3, 4, 6, 11, 13, 14]
    default_outputs = [2, 5, 7, 10, 12, 15]

    test_sync = TestLogic("Synchronous operation", default_inputs, default_outputs,
        body=[
            [[1, '/',  0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            [[1, '/',  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            [[1, '/',  0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            [[1, '/',  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
        ]
    )
    test_async = TestLogic("Asynchronous operation", default_inputs, default_outputs,
        body=[
            # clear
            [[0, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            # load 1s
            [[1, 1,  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            # clear
            [[0, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
            [[1, 0,  1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]],
        ]
    )

    tests = [test_sync, test_async]
