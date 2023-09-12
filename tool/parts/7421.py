from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part7421(PackageDIP14):
    name = "7421"
    desc = "Dual 4-input positive-AND gates"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("NC", PinType.NC),
        4: Pin("1C", PinType.IN),
        5: Pin("1D", PinType.IN),
        6: Pin("1Y", PinType.OUT),
        8: Pin("2Y", PinType.OUT),
        9: Pin("2A", PinType.IN),
        10: Pin("2B", PinType.IN),
        11: Pin("NC", PinType.NC),
        12: Pin("2C", PinType.IN),
        13: Pin("2D", PinType.IN),
    }

    tests = [
        Test("Complete logic", Test.LOGIC,
            inputs=[1, 2, 4, 5, 13, 12, 10, 9],
            outputs=[6, 8],
            body=[[2*x, 2*[x.vand()]] for x in BV.range(0, 16)]
        )
    ]
