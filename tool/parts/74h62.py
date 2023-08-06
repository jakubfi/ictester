from binvec import BV
from prototypes import (PackageDIP14, Pin, Test)

'''
NOTE on testing expanders:
~X and X are outputs, but not in a TTL-levels sense: ~X is output transistor collector, X is its emmiter.
Pin configuration does the following:
 * pulls up the collector with the internal pull-up resistor (OC output)
 * connects the emmiter to a current sink (output driven low)
Thus, ~X becomes the actual output, and X needs to be always driven low.
'''

class Part74H62(PackageDIP14):
    name = "74H62"
    desc = "AND-OR Gate Expander"
    pin_cfg = {
        1: Pin("A", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("C", Pin.IN),
        4: Pin("D", Pin.IN),
        5: Pin("E", Pin.IN),
        6: Pin("~X", Pin.OC),
        8: Pin("X", Pin.IN),
        9: Pin("F", Pin.IN),
        10: Pin("G", Pin.IN),
        11: Pin("H", Pin.IN),
        12: Pin("I", Pin.IN),
        13: Pin("J", Pin.IN),
    }

    test_async = Test("Asynchronous operation", Test.COMB,
        inputs=[8,  1, 2,  3, 4, 5,  9, 10, 11,  12, 13],
        outputs=[6],
        loops=64,
        body=lambda: [
            [[0, *ab, *cde, *fgh, *ij],  ~(ab.vand() | cde.vand() | fgh.vand() | ij.vand())]
            for ab in BV.range(0, 4)
            for cde in BV.range(0, 8)
            for fgh in BV.range(0, 8)
            for ij in BV.range(0, 4)
        ]
    )

    tests = [test_async]
