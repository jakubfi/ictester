from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part7430(PackageDIP14):
    name = "7430"
    desc = "8-input positive-NAND gate"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("C", PinType.IN),
        4: Pin("D", PinType.IN),
        5: Pin("E", PinType.IN),
        6: Pin("F", PinType.IN),
        8: Pin("Y", PinType.OUT),
        9: Pin("NC", PinType.NC),
        10: Pin("NC", PinType.NC),
        11: Pin("G", PinType.IN),
        12: Pin("H", PinType.IN),
        13: Pin("NC", PinType.NC),
    }

    tests = [
        TestLogic("Complete logic",
            inputs=[1, 2, 3, 4, 5, 6, 11, 12],
            outputs=[8],
            body=[[x, [not x.vand()]] for x in BV.range(0, 2**8)]
        )
    ]
