from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74H61(PackageDIP14):
    name = "74H61"
    desc = "Triple 3-input expanders"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("1C", PinType.IN),
        4: Pin("2A", PinType.IN),
        5: Pin("2B", PinType.IN),
        6: Pin("2C", PinType.IN),
        8: Pin("2X", PinType.OC),
        9: Pin("1X", PinType.OC),
        10: Pin("3X", PinType.OC),
        11: Pin("3A", PinType.IN),
        12: Pin("3B", PinType.IN),
        13: Pin("3C", PinType.IN),
    }

    test_async = Test("Asynchronous operation", Test.LOGIC,
        inputs=[1, 2, 3,  4, 5, 6,  11, 12, 13],
        outputs=[9, 8, 10],
        loops=64,
        body=[
            [[*g1, *g2, *g3], [not g1.vand(), not g2.vand(), not g3.vand()]]
            for g1 in BV.range(0, 2**3)
            for g2 in BV.range(0, 2**3)
            for g3 in BV.range(0, 2**3)
        ]
    )

    tests = [test_async]
