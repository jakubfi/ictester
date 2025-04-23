from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74138(PackageDIP16):
    name = "74138"
    desc = "3-line to 8-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("C", PinType.IN),
        4: Pin("~G2A", PinType.IN),
        5: Pin("~G2B", PinType.IN),
        6: Pin("G1", PinType.IN),
        7: Pin("Y7", PinType.OUT),
        9: Pin("Y6", PinType.OUT),
        10: Pin("Y5", PinType.OUT),
        11: Pin("Y4", PinType.OUT),
        12: Pin("Y3", PinType.OUT),
        13: Pin("Y2", PinType.OUT),
        14: Pin("Y1", PinType.OUT),
        15: Pin("Y0", PinType.OUT),
    }

    test_enabled = TestLogic("Enabled",
        inputs=[3, 2, 1,  6, 4, 5],
        outputs=[7, 9, 10, 11, 12, 13, 14, 15],
        body=[
            [[*BV.int(addr, 3), 1, 0, 0], [*~BV.bit(addr, 8)]]
            for addr in range(0, 8)
        ]
    )

    test_g1 = TestLogic("G1 disabled",
        inputs=[1, 2, 3,  6, 4, 5],
        outputs=[15, 14, 13, 12, 11, 10, 9, 7],
        body=[
            [[0, 0, 0,  0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0,  0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0,  0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0,  0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )

    test_g2 = TestLogic("G2 disabled",
        inputs=[1, 2, 3,  6, 4, 5],
        outputs=[15, 14, 13, 12, 11, 10, 9, 7],
        body=[
            [[0, 0, 0,  1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0,  1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0,  1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )

    tests = [test_enabled, test_g1, test_g2]
