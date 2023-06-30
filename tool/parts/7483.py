from binvec import BV
from prototypes import (PackageDIP16_vcc5, Pin, Test)

class Part7483(PackageDIP16_vcc5):
    name = "7483"
    desc = "4-bit binary full adder with fast carry"
    pin_cfg = {
        1: Pin("A4", Pin.IN),
        2: Pin("S3", Pin.OUT),
        3: Pin("A3", Pin.IN),
        4: Pin("B3", Pin.IN),
        6: Pin("S2", Pin.OUT),
        7: Pin("B2", Pin.IN),
        8: Pin("A2", Pin.IN),
        9: Pin("S1", Pin.OUT),
        10: Pin("A1", Pin.IN),
        11: Pin("B1", Pin.IN),
        13: Pin("C0", Pin.IN),
        14: Pin("C4", Pin.OUT),
        15: Pin("S4", Pin.OUT),
        16: Pin("B4", Pin.IN),
    }

    test_all = Test("Complete logic", Test.COMB,
        inputs=[13,  1, 3, 8, 10,  16, 4, 7, 11],
        outputs=[15, 2, 6, 9,  14],
        body=lambda: [
            [[*c, *a, *b],  [*(a+b+c), (a+b+c).carry]]
            for a in BV.range(0, 16)
            for b in BV.range(0, 16)
            for c in BV.range(0, 2)
        ]
    )

    tests = [test_all]
