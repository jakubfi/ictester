from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

'''
NOTE on testing expanders:
~X and X are outputs, but not in a TTL-levels sense: ~X is output transistor collector, X is its emmiter.
Pin configuration does the following:
 * pulls up the collector with the internal pull-up resistor (OC output)
 * connects the emmiter to a current sink (output driven low)
Thus, ~X becomes the actual output, and X needs to be always driven low.
'''

class Part7460(PackageDIP14):
    name = "7460"
    desc = "Dual 4-input expanders"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("1C", PinType.IN),
        4: Pin("2A", PinType.IN),
        5: Pin("2B", PinType.IN),
        6: Pin("2C", PinType.IN),
        8: Pin("2D", PinType.IN),
        9: Pin("~2X", PinType.OC),
        10: Pin("2X", PinType.IN),
        11: Pin("1X", PinType.IN),
        12: Pin("~1X", PinType.OC),
        13: Pin("1D", PinType.IN),
    }

    test_async = TestLogic("Asynchronous operation",
        inputs=[11, 10,  1, 2, 3, 13,  4, 5, 6, 8],
        outputs=[12, 9],
        body = [
            [[0, 0, *g1, *g2],  [not g1.vand(), not g2.vand()]]
            for g1 in BV.range(0, 2**4)
            for g2 in BV.range(0, 2**4)
        ]
    )

    tests = [test_async]
