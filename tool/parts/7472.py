from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part7472(PackageDIP14):
    name = "7472"
    desc = "And-gated J-K master-slave flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("NC", PinType.NC),
        2: Pin("~CLR", PinType.IN),
        3: Pin("J1", PinType.IN),
        4: Pin("J2", PinType.IN),
        5: Pin("J3", PinType.IN),
        6: Pin("~Q", PinType.OUT),
        8: Pin("Q", PinType.OUT),
        9: Pin("K1", PinType.IN),
        10: Pin("K2", PinType.IN),
        11: Pin("K3", PinType.IN),
        12: Pin("CLK", PinType.IN),
        13: Pin("~PRE", PinType.IN),
    }

    default_inputs = [3, 4, 5,  9, 10, 11,  13, 2, 12]
    default_outputs = [8, 6]

    test_sync = TestLogic("Load, clear, toogle, keep", default_inputs, default_outputs,
        body=[
            # load 1
            [[1, 1, 1,  0, 0, 0,  1, 1, '\\'], [1, 0]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '\\'], [1, 0]],
            # load 0
            [[0, 0, 0,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '\\'], [0, 1]],
            # toggle
            [[1, 1, 1,  1, 1, 1,  1, 1, '\\'], [1, 0]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '\\'], [1, 0]],
            # toggle
            [[1, 1, 1,  1, 1, 1,  1, 1, '\\'], [0, 1]],
        ]
    )
    test_async = TestLogic("Set, preset", default_inputs, default_outputs,
        body=[
            [[0, 0, 0,  1, 1, 1,  0, 1, '\\'], [1, 0]],
            [[1, 1, 1,  0, 0, 0,  1, 0, '\\'], [0, 1]],
            [[0, 0, 0,  1, 1, 1,  0, 1, '\\'], [1, 0]],
            [[1, 1, 1,  0, 0, 0,  1, 0, '\\'], [0, 1]],
            [[1, 1, 1,  1, 1, 1,  0, 1, '\\'], [1, 0]],
            [[1, 1, 1,  1, 1, 1,  1, 0, '\\'], [0, 1]],
            [[0, 0, 0,  0, 0, 0,  0, 1, '\\'], [1, 0]],
            [[0, 0, 0,  0, 0, 0,  1, 0, '\\'], [0, 1]],
        ]
    )
    test_and = TestLogic("And input gates", default_inputs, default_outputs,
        body=[
            # try J=1 with not fully set K
            [[1, 1, 1,  0, 0, 0,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  0, 0, 1,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  0, 1, 0,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  0, 1, 1,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  1, 0, 0,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  1, 0, 1,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  1, 1, 0,  1, 1, '\\'], [1, 0]],
            [[1, 1, 1,  1, 1, 1,  1, 1, '\\'], [0, 1]],

            # clear
            [[1, 1, 1,  0, 0, 0,  1, 0, '\\'], [0, 1]],

            # try K=1 with not fully set J
            [[0, 0, 0,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[0, 0, 1,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[0, 1, 0,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[0, 1, 1,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[1, 0, 0,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[1, 0, 1,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[1, 1, 0,  1, 1, 1,  1, 1, '\\'], [0, 1]],
            [[1, 1, 1,  1, 1, 1,  1, 1, '\\'], [1, 0]],
        ]
    )

    tests = [test_sync, test_async, test_and]
