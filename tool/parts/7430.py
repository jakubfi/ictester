from binvec import BV
from prototypes import (PackageDIP14, Pin, Test)

class Part7430(PackageDIP14):
    name = "7430"
    desc = "8-input positive-NAND gate"
    pin_cfg = {
        1: Pin("A", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("C", Pin.IN),
        4: Pin("D", Pin.IN),
        5: Pin("E", Pin.IN),
        6: Pin("F", Pin.IN),
        8: Pin("Y", Pin.OUT),
        9: Pin("NC", Pin.NC),
        10: Pin("NC", Pin.NC),
        11: Pin("G", Pin.IN),
        12: Pin("H", Pin.IN),
        13: Pin("NC", Pin.NC),
    }

    tests = [
        Test("Complete logic", Test.COMB,
            inputs=[1, 2, 3, 4, 5, 6, 11, 12],
            outputs=[8],
            body=[[x, ~x.vand()] for x in BV.range(0, 256)]
        )
    ]
