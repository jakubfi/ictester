from prototypes import (PackageDIP14, Pin, PinType, TestLogic)
from binvec import BV

class Part74125(PackageDIP14):
    name = "74125"
    desc = "Quarduple bus buffers with 3-state outputs"
    pin_cfg = {
        1: Pin("~1G", PinType.IN),
        2: Pin("1A", PinType.IN),
        3: Pin("1Y", PinType.ST3),
        4: Pin("~2G", PinType.IN),
        5: Pin("2A", PinType.IN),
        6: Pin("2Y", PinType.ST3),
        8: Pin("3Y", PinType.ST3),
        9: Pin("3A", PinType.IN),
        10: Pin("~3G", PinType.IN),
        11: Pin("4Y", PinType.ST3),
        12: Pin("4A", PinType.IN),
        13: Pin("~4G", PinType.IN),
    }

    test_enabled = TestLogic("Outputs enabled",
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[0, 0, 0, 0, *v], v]
            for v in BV.range(0, 2**4)
        ]
    )

    test_disabled = TestLogic("Outputs disabled",
        read_delay_us=2,  # switching to HiZ with 5k pullups requires some time
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[1, 1, 1, 1, *v], [1, 1, 1, 1]]
            for v in BV.range(0, 2**4)
        ]
    )

    test_switching = TestLogic("Switching outputs",
        read_delay_us=2,  # switching to HiZ with 5k pullups requires some time
        loops=512,
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[*ena, *v], v | ena]
            for v in BV.range(0, 2**4)
            for ena in BV.range(0, 2**4)
        ]
    )

    tests = [test_enabled, test_disabled, test_switching]
