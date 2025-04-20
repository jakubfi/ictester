from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType, ZIFFunc)
from ictester.test import TestLogic

out_funcs = [ZIFFunc.IN_HIZ, ZIFFunc.IN_PU_STRONG]

class Part74126(PackageDIP14):
    name = "74126"
    desc = "Quarduple bus buffers with 3-state outputs"
    pin_cfg = {
        1: Pin("~1G", PinType.IN),
        2: Pin("1A", PinType.IN),
        3: Pin("1Y", PinType.ST3, zif_func=out_funcs),
        4: Pin("~2G", PinType.IN),
        5: Pin("2A", PinType.IN),
        6: Pin("2Y", PinType.ST3, zif_func=out_funcs),
        8: Pin("3Y", PinType.ST3, zif_func=out_funcs),
        9: Pin("3A", PinType.IN),
        10: Pin("~3G", PinType.IN),
        11: Pin("4Y", PinType.ST3, zif_func=out_funcs),
        12: Pin("4A", PinType.IN),
        13: Pin("~4G", PinType.IN),
    }

    test_high = TestLogic("Switching outputs, ext. pulled high",
        cfgnum=1,
        loops=512,
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=(
            [[*ena, *v], v | ~ena]
            for v in BV.range(0, 2**4)
            for ena in BV.range(0, 2**4)
        )
    )

    test_low = TestLogic("Switching outputs, ext. pulled low",
        cfgnum=0,
        read_delay_us=45,  # it takes time with 1M pull-downs
        loops=128,
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=(
            [[*ena, *v], v & ena]
            for v in BV.range(0, 2**4)
            for ena in BV.range(0, 2**4)
        )
    )

    tests = [test_high, test_low]
