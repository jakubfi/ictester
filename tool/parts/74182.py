from binvec import BV
from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part74182(PackageDIP16):
    name = "74182"
    desc = "Look-ahead carry generator"
    pin_cfg = {
        1: Pin("~G1", PinType.IN),
        2: Pin("~P1", PinType.IN),
        3: Pin("~G0", PinType.IN),
        4: Pin("~P0", PinType.IN),
        5: Pin("~G3", PinType.IN),
        6: Pin("~P3", PinType.IN),
        7: Pin("~P", PinType.OUT),
        9: Pin("Cn+z", PinType.OUT),
        10: Pin("~G", PinType.OUT),
        11: Pin("Cn+y", PinType.OUT),
        12: Pin("Cn+x", PinType.OUT),
        13: Pin("Cn", PinType.IN),
        14: Pin("~G2", PinType.IN),
        15: Pin("~P2", PinType.IN),
    }

    test_g = TestLogic("~G",
        inputs=[5, 14, 1, 3, 6, 15, 2],
        outputs=[10],
        loops=64,
        body=[
            [
                v, [0] if not v[0]
                or (not v[1] and not v[4])
                or (not v[2] and v[4:6] == [0, 0])
                or v[3:] == [0, 0, 0, 0]
                else [1]
            ]
            for v in BV.range(0, 128)
        ]
    )
    test_p = TestLogic("~P",
        inputs=[2, 4, 6, 15],
        outputs=[7],
        loops=64,
        body=[
            [v, [0] if v == [0, 0, 0, 0] else [1]]
            for v in BV.range(0, 16)
        ]
    )
    test_cnx = TestLogic("Cn+x",
        inputs=[3, 4, 13],
        outputs=[12],
        loops=64,
        body=[
            [v, [1] if not v[0] or v[1:3] == [0, 1] else [0]]
            for v in BV.range(0, 8)
        ]
    )
    test_cny = TestLogic("Cn+y",
        inputs=[1, 3, 2, 4, 13],
        outputs=[11],
        loops=64,
        body=[
            [v, [1] if not v[0] or v[1:3] == [0, 0] or v[2:5] == [0, 0, 1] else [0]]
            for v in BV.range(0, 32)
        ]
    )
    test_cnz = TestLogic("Cn+z",
        inputs=[14, 1, 3, 15, 2, 4, 13],
        outputs=[9],
        loops=64,
        body=[
            [v, [1] if not v[0] or (not v[1] and not v[3]) or v[2:5] == [0, 0, 0] or v[3:] == [0, 0, 0, 1] else [0]]
            for v in BV.range(0, 128)
        ]
    )

    tests = [test_g, test_p, test_cnx, test_cny, test_cnz]
