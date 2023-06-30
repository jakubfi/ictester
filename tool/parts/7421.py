from binvec import BV
from prototypes import (PackageDIP14, Pin, Test)

class Part7421(PackageDIP14):
    name = "7421"
    desc = "Dual 4-input positive-AND gates"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1B", Pin.IN),
        3: Pin("NC", Pin.NC),
        4: Pin("1C", Pin.IN),
        5: Pin("1D", Pin.IN),
        6: Pin("1Y", Pin.OUT),
        8: Pin("2Y", Pin.OUT),
        9: Pin("2A", Pin.IN),
        10: Pin("2B", Pin.IN),
        11: Pin("NC", Pin.NC),
        12: Pin("2C", Pin.IN),
        13: Pin("2D", Pin.IN),
    }

    tests = [
        Test("Complete logic", Test.COMB,
            inputs=[1, 2, 4, 5, 13, 12, 10, 9],
            outputs=[6, 8],
            body=[[2*x, 2*x.vand()] for x in BV.range(0, 16)]
        )
    ]
