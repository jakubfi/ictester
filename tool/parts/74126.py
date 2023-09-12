from prototypes import (PackageDIP14, Pin, PinType, Test)
from binvec import BV

class Part74126(PackageDIP14):
    name = "74126"
    desc = "Quarduple bus buffers with 3-state outputs"
    pin_cfg = {
        1: Pin("1G", PinType.IN),
        2: Pin("1A", PinType.IN),
        3: Pin("1Y", PinType.ST3),
        4: Pin("2G", PinType.IN),
        5: Pin("2A", PinType.IN),
        6: Pin("2Y", PinType.ST3),
        8: Pin("3Y", PinType.ST3),
        9: Pin("3A", PinType.IN),
        10: Pin("3G", PinType.IN),
        11: Pin("4Y", PinType.ST3),
        12: Pin("4A", PinType.IN),
        13: Pin("4G", PinType.IN),
    }

    # switching to HiZ with 5k pullups requires some time
    read_delay_us = 2

    test_all = Test("Complete logic", Test.LOGIC,
        params=list(round(read_delay_us/0.2).to_bytes(2, 'little')),
        inputs=[1, 4, 10, 13,  2, 5, 9, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[*ena, *v], v|~ena]
            for v in BV.range(0, 2**4)
            for ena in BV.range(0, 2**4)
        ]
    )

    tests = [test_all]

