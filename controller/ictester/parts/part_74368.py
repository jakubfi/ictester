from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType, ZIFFunc)
from ictester.test import TestLogic

out_funcs = [ZIFFunc.IN_HIZ, ZIFFunc.IN_PU_STRONG]

class Part74368(PackageDIP16):
    name = "74368"
    desc = "Hex Bus Drivers with 3-state Outputs"
    pin_cfg = {
        1: Pin("~1G", PinType.IN),
        2: Pin("1A1", PinType.IN),
        3: Pin("1Y1", PinType.ST3, zif_func=out_funcs),
        4: Pin("1A2", PinType.IN),
        5: Pin("1Y2", PinType.ST3, zif_func=out_funcs),
        6: Pin("1A3", PinType.IN),
        7: Pin("1Y3", PinType.ST3, zif_func=out_funcs),
        9: Pin("1Y4", PinType.ST3, zif_func=out_funcs),
        10: Pin("1A4", PinType.IN),
        11: Pin("2Y1", PinType.ST3, zif_func=out_funcs),
        12: Pin("2A1", PinType.IN),
        13: Pin("2Y2", PinType.ST3, zif_func=out_funcs),
        14: Pin("2A2", PinType.IN),
        15: Pin("~2G", PinType.IN),
    }

    test_enabled = TestLogic("Outputs enabled",
        cfgnum=0,
        inputs=[1, 15,  2, 4, 6, 10, 12, 14],
        outputs=[3, 5, 7, 9, 11, 13],
        body=lambda: [
            [[0, 0, *x], ~x] for x in BV.range(0, 2**6)
        ]
    )

    test_disabled_low = TestLogic("Outputs disabled, ext. pulled low",
        cfgnum=0,
        inputs=[1, 15,  2, 4, 6, 10, 12, 14],
        outputs=[3, 5, 7, 9, 11, 13],
        body=lambda: [
            [[1, 1, *x], 6*[0]] for x in BV.range(0, 2**6)
        ]
    )

    test_disabled_high = TestLogic("Outputs disabled, ext. pulled high",
        cfgnum=1,
        inputs=[1, 15,  2, 4, 6, 10, 12, 14],
        outputs=[3, 5, 7, 9, 11, 13],
        body=lambda: [
            [[1, 1, *x], 6*[1]] for x in BV.range(0, 2**6)
        ]
    )

    tests = [test_enabled, test_disabled_low, test_disabled_high]
