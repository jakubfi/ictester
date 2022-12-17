from functools import reduce
from prototypes import (PackageDIP14, Pin, Test)

class Part74180(PackageDIP14):
    name = "74180"
    desc = "9-bit odd/even parity generator/checker"
    pin_cfg = {
        1: Pin("G", Pin.IN),
        2: Pin("H", Pin.IN),
        3: Pin("EVEN", Pin.IN),
        4: Pin("ODD", Pin.IN),
        5: Pin("sumEVEN", Pin.OUT),
        6: Pin("sumODD", Pin.OUT),
        8: Pin("A", Pin.IN),
        9: Pin("B", Pin.IN),
        10: Pin("C", Pin.IN),
        11: Pin("D", Pin.IN),
        12: Pin("E", Pin.IN),
        13: Pin("F", Pin.IN),
    }

    # ------------------------------------------------------------------------
    def parity_test_gen():
        # ------------------------------------------------------------------------
        def parity_check(v):
            if v[8] == v[9]:
                return [int(not v[8]), int(not v[8])]
            else:
                odd = reduce(lambda a, b: a^b, v[0:8] + [v[9]])
                return [int(not odd), odd]

        data = [Test.bin2vec(v, 10) for v in range(0, 2**10 - 1)]

        body = [
            [v, parity_check(v)] for v in data
        ]

        return Test(
            name="Asynchronous operation",
            inputs=[8, 9, 10, 11, 12, 13, 1, 2,  3, 4],
            outputs=[5, 6],
            ttype=Test.COMB,
            loops=64,
            body=body
        )

    tests = [parity_test_gen()]