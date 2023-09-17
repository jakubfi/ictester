from binvec import BV
from prototypes import (PackageDIP16_vcc5, Pin, PinType, TestLogic)

class Part7483(PackageDIP16_vcc5):
    name = "7483"
    desc = "4-bit binary full adder with fast carry"
    pin_cfg = {
        1: Pin("A4", PinType.IN),
        2: Pin("S3", PinType.OUT),
        3: Pin("A3", PinType.IN),
        4: Pin("B3", PinType.IN),
        6: Pin("S2", PinType.OUT),
        7: Pin("B2", PinType.IN),
        8: Pin("A2", PinType.IN),
        9: Pin("S1", PinType.OUT),
        10: Pin("A1", PinType.IN),
        11: Pin("B1", PinType.IN),
        13: Pin("C0", PinType.IN),
        14: Pin("C4", PinType.OUT),
        15: Pin("S4", PinType.OUT),
        16: Pin("B4", PinType.IN),
    }

    test_all = TestLogic("Complete logic",
        inputs=[13,  1, 3, 8, 10,  16, 4, 7, 11],
        outputs=[15, 2, 6, 9,  14],
        body=lambda: [
            [[*c, *a, *b],  [*(a+b+c), (a+b+c).carry]]
            for a in BV.range(0, 2**4)
            for b in BV.range(0, 2**4)
            for c in BV.range(0, 2)
        ]
    )

    tests = [test_all]
