from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part7447(PackageDIP16):
    name = "7447"
    desc = "BCD-to-seven-segment decoders/drivers"
    pin_cfg = {
        1: Pin("B", PinType.IN),
        2: Pin("C", PinType.IN),
        3: Pin("~LT", PinType.IN),
        4: Pin("~BI/~RBO", PinType.IN),
        5: Pin("~RBI", PinType.IN),
        6: Pin("D", PinType.IN),
        7: Pin("A", PinType.IN),
        9: Pin("e", PinType.OC),
        10: Pin("d", PinType.OC),
        11: Pin("c", PinType.OC),
        12: Pin("b", PinType.OC),
        13: Pin("a", PinType.OC),
        14: Pin("g", PinType.OC),
        15: Pin("f", PinType.OC),
    }

    # TODO: full coverage
    test_async = TestLogic("Asynchronous operation",
        read_delay_us=2,  # 7447 outputs are very slow, signal rise is ~5us
        inputs=[6, 2, 1, 7,  3, 5, 4],
        outputs=[13, 12, 11, 10, 9, 15, 14],
        body=[
            # symbols
            [[0, 0, 0, 0,  1, 1, 1], [0, 0, 0, 0, 0, 0, 1]],
            [[0, 0, 0, 1,  1, 1, 1], [1, 0, 0, 1, 1, 1, 1]],
            [[0, 0, 1, 0,  1, 1, 1], [0, 0, 1, 0, 0, 1, 0]],
            [[0, 0, 1, 1,  1, 1, 1], [0, 0, 0, 0, 1, 1, 0]],
            [[0, 1, 0, 0,  1, 1, 1], [1, 0, 0, 1, 1, 0, 0]],
            [[0, 1, 0, 1,  1, 1, 1], [0, 1, 0, 0, 1, 0, 0]],
            [[0, 1, 1, 0,  1, 1, 1], [1, 1, 0, 0, 0, 0, 0]],
            [[0, 1, 1, 1,  1, 1, 1], [0, 0, 0, 1, 1, 1, 1]],
            [[1, 0, 0, 0,  1, 1, 1], [0, 0, 0, 0, 0, 0, 0]],
            [[1, 0, 0, 1,  1, 1, 1], [0, 0, 0, 1, 1, 0, 0]],
            [[1, 0, 1, 0,  1, 1, 1], [1, 1, 1, 0, 0, 1, 0]],
            [[1, 0, 1, 1,  1, 1, 1], [1, 1, 0, 0, 1, 1, 0]],
            [[1, 1, 0, 0,  1, 1, 1], [1, 0, 1, 1, 1, 0, 0]],
            [[1, 1, 0, 1,  1, 1, 1], [0, 1, 1, 0, 1, 0, 0]],
            [[1, 1, 1, 0,  1, 1, 1], [1, 1, 1, 0, 0, 0, 0]],
            [[1, 1, 1, 1,  1, 1, 1], [1, 1, 1, 1, 1, 1, 1]],
            # BI/RBI
            [[0, 0, 0, 0,  1, 1, 0], [1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0, 0,  1, 0, 0], [1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0, 0,  0, 1, 0], [1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0, 0,  0, 0, 0], [1, 1, 1, 1, 1, 1, 1]],
            # LT
            [[1, 1, 1, 1,  0, 0, 1], [0, 0, 0, 0, 0, 0, 0]],
            [[1, 1, 1, 1,  0, 1, 1], [0, 0, 0, 0, 0, 0, 0]],
        ]
    )

    tests = [test_async]
