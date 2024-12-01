from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

class Part7474(PackageDIP14):
    name = "7474"
    desc = "Dual D-type positive-edge-triggered flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("~1CLR", PinType.IN),
        2: Pin("1D", PinType.IN),
        3: Pin("1CLK", PinType.IN),
        4: Pin("~1PRE", PinType.IN),
        5: Pin("1Q", PinType.OUT),
        6: Pin("~1Q", PinType.OUT),
        8: Pin("~2Q", PinType.OUT),
        9: Pin("2Q", PinType.OUT),
        10: Pin("~2PRE", PinType.IN),
        11: Pin("2CLK", PinType.IN),
        12: Pin("2D", PinType.IN),
        13: Pin("~2CLR", PinType.IN),
    }

    default_inputs = [1, 4, 2, 3, 13, 10, 12, 11]
    default_outputs = [5, 6, 9, 8]

    test_sync = TestLogic("Synchronous operation", default_inputs, default_outputs,
        body=[
            [[1, 1, 0, '/',  1, 1, 0, '/'], [0, 1,  0, 1]],
            [[1, 1, 1, '/',  1, 1, 1, '/'], [1, 0,  1, 0]],
        ]
    )
    test_async = TestLogic("Asynchronous operation", default_inputs, default_outputs,
        body=[
            [[0, 1, 0, 0,  0, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 0, 0, 0,  1, 0, 0, 0], [1, 0,  1, 0]],
        ]
    )

    tests = [test_sync, test_async]
