from ictester.part import (PackageDIP16, Pin, PinType, ZIFFunc)
from ictester.test import TestLogic

out_funcs = [ZIFFunc.IN_HIZ, ZIFFunc.IN_PU_STRONG]

class Part74173(PackageDIP16):
    name = "74173"
    desc = "4-bit D-type registers with 3-state outputs"
    pin_cfg = {
        1: Pin("M", PinType.IN),
        2: Pin("N", PinType.IN),
        3: Pin("1Q", PinType.ST3, zif_func=out_funcs),
        4: Pin("2Q", PinType.ST3, zif_func=out_funcs),
        5: Pin("3Q", PinType.ST3, zif_func=out_funcs),
        6: Pin("4Q", PinType.ST3, zif_func=out_funcs),
        7: Pin("CLK", PinType.IN),
        9: Pin("~G1", PinType.IN),
        10: Pin("~G2", PinType.IN),
        11: Pin("4D", PinType.IN),
        12: Pin("3D", PinType.IN),
        13: Pin("2D", PinType.IN),
        14: Pin("1D", PinType.IN),
        15: Pin("CLR", PinType.IN),
    }

    test_load = TestLogic("Loads, gated, clear",
        cfgnum=0,
        inputs=[15,  1, 2,  9, 10,  7,  14, 13, 12, 11],
        outputs=[3, 4, 5, 6],
        body=[
            # load 1
            [[0,  0, 0,  0, 0,  '/',  1, 1, 1, 1], [1, 1, 1, 1]],
            # load 0
            [[0,  0, 0,  0, 0,  '/',  0, 0, 0, 0], [0, 0, 0, 0]],
            # load 1 inhibited
            [[0,  0, 0,  0, 1,  '/',  1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 0,  1, 0,  '/',  1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 0,  1, 1,  '/',  1, 1, 1, 1], [0, 0, 0, 0]],
            # load 1
            [[0,  0, 0,  0, 0,  '/',  1, 1, 1, 1], [1, 1, 1, 1]],
            # load 0 inhibited
            [[0,  0, 0,  0, 1,  '/',  0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 0,  1, 0,  '/',  0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 0,  1, 1,  '/',  0, 0, 0, 0], [1, 1, 1, 1]],
            # clear
            [['/',  0, 0,  0, 0,  '/',  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )

    test_disabled_low = TestLogic("Outputs disabled, ext. pulled low",
        cfgnum=0,
        read_delay_us=55,  # it takes time with 1M pull-downs
        loops=256,
        inputs=[15,  1, 2,  9, 10,  7,  14, 13, 12, 11],
        outputs=[3, 4, 5, 6],
        body=[
            # load 1
            [[0,  0, 0,  0, 0,  '+',  1, 1, 1, 1], [1, 1, 1, 1]],
            # inhibit/enable
            [[0,  1, 1,  0, 0,   0,   0, 0, 0, 0], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 1,  0, 0,   0,   0, 0, 0, 0], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  1, 0,  0, 0,   0,   0, 0, 0, 0], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            # load 0
            [[0,  0, 0,  0, 0,  '+',  0, 0, 0, 0], [0, 0, 0, 0]],
            # inhibit/enable
            [[0,  1, 1,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 1,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  1, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )

    test_disabled_high = TestLogic("Outputs disabled, ext. pulled high",
        cfgnum=1,
        inputs=[15,  1, 2,  9, 10,  7,  14, 13, 12, 11],
        outputs=[3, 4, 5, 6],
        body=[
            # load 1
            [[0,  0, 0,  0, 0,  '+',  1, 1, 1, 1], [1, 1, 1, 1]],
            [[0,  1, 1,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 1,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  1, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   0, 0, 0, 0], [1, 1, 1, 1]],
            # load 0
            [[0,  0, 0,  0, 0,  '+',  0, 0, 0, 0], [0, 0, 0, 0]],
            [[0,  1, 1,  0, 0,   0,   1, 1, 1, 1], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  0, 1,  0, 0,   0,   1, 1, 1, 1], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
            [[0,  1, 0,  0, 0,   0,   1, 1, 1, 1], [1, 1, 1, 1]],
            [[0,  0, 0,  0, 0,   0,   1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )

    tests = [test_load, test_disabled_low, test_disabled_high]
