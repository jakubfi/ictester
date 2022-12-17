from collections import namedtuple
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

    # ------------------------------------------------------------------------
    def add_test_gen():
        Vector = namedtuple('Vector', ['a', 'b', 'c', 'f'])

        # raw, numerical test data
        data = [
            Vector(a, b, c, a + b + c)
            for a in range(0, 16)
            for b in range(0, 16)
            for c in range(0, 2)
        ]

        # test vectors in [[inputs], [outputs]] order:
        # [[cin, a4, a3, a2, a1,  b4, b3, b2, b1], [f4, f3, f2, f1,  cout]]
        body = [
            [
                [v.c] + Test.bin2vec(v.a, 4) + Test.bin2vec(v.b, 4),
                Test.bin2vec(v.f & 0b1111, 4) + [True if v.f & 0b10000 else False]
            ]
            for v in data
        ]
        return body

    test_all = Test(
        name="Complete logic",
        inputs=[13,  1, 3, 8, 10,  16, 4, 7, 11],
        outputs=[15, 2, 6, 9,  14],
        ttype=Test.COMB,
        body=add_test_gen()
    )
    tests = [test_all]
