from binvec import BV
from part import (PackageDIP14, Pin, PinType)
from test import TestLogic

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
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("C", PinType.IN),
        4: Pin("D", PinType.IN),
        5: Pin("E", PinType.IN),
        6: Pin("~X", PinType.OC),
        8: Pin("X", PinType.IN),
        9: Pin("F", PinType.IN),
        10: Pin("G", PinType.IN),
        11: Pin("H", PinType.IN),
        12: Pin("I", PinType.IN),
        13: Pin("J", PinType.IN),
    }

    test_async = TestLogic("Asynchronous operation",
        inputs=[8,  1, 2,  3, 4, 5,  9, 10, 11,  12, 13],
        outputs=[6],
        loops=64,
        body=lambda: [
            [[0, *ab, *cde, *fgh, *ij],  [not (ab.vand() or cde.vand() or fgh.vand() or ij.vand())]]
            for ab in BV.range(0, 2**2)
            for cde in BV.range(0, 2**3)
            for fgh in BV.range(0, 2**3)
            for ij in BV.range(0, 2**2)
        ]
    )

    tests = [test_async]
