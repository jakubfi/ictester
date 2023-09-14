from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part7400(PackageDIP14):
    name = "7400"
    desc = "Quad 2-input positive-NAND gates"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("1Y", PinType.OUT),
        4: Pin("2A", PinType.IN),
        5: Pin("2B", PinType.IN),
        6: Pin("2Y", PinType.OUT),
        8: Pin("3Y", PinType.OUT),
        9: Pin("3A", PinType.IN),
        10: Pin("3B", PinType.IN),
        11: Pin("4Y", PinType.OUT),
        12: Pin("4A", PinType.IN),
        13: Pin("4B", PinType.IN),
    }

    tests = [
        Test("Complete logic", Test.LOGIC,
            inputs=[1, 2, 4, 5, 9, 10, 12, 13],
            outputs=[3, 6, 8, 11],
            body=[
                [[*g1, *g2, *g3, *g4], [not g1.vand(), not g2.vand(), not g3.vand(), not g4.vand()]]
                for g1 in BV.range(0, 2**2)
                for g2 in BV.range(0, 2**2)
                for g3 in BV.range(0, 2**2)
                for g4 in BV.range(0, 2**2)
            ]
        )
    ]


