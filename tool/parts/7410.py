from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part7410(PackageDIP14):
    name = "7410"
    desc = "Triple 3-input positive-NAND gates"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("2A", PinType.IN),
        4: Pin("2B", PinType.IN),
        5: Pin("2C", PinType.IN),
        6: Pin("2Y", PinType.OUT),
        8: Pin("3Y", PinType.OUT),
        9: Pin("3A", PinType.IN),
        10: Pin("3B", PinType.IN),
        11: Pin("3C", PinType.IN),
        12: Pin("1Y", PinType.OUT),
        13: Pin("1C", PinType.IN),
    }

    tests = [
        TestLogic("Complete logic",
            inputs=[1, 2, 13, 3, 4, 5, 9, 10, 11],
            outputs=[12, 6, 8],
            body=[
                [[*g1, *g2, *g3], [not g1.vand(), not g2.vand(), not g3.vand()]]
                for g1 in BV.range(0, 2**3)
                for g2 in BV.range(0, 2**3)
                for g3 in BV.range(0, 2**3)
            ]
        )
    ]
