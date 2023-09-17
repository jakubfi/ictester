from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part7404(PackageDIP14):
    name = "7404"
    desc = "Hex inverters"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1Y", PinType.OUT),
        3: Pin("2A", PinType.IN),
        4: Pin("2Y", PinType.OUT),
        5: Pin("3A", PinType.IN),
        6: Pin("3Y", PinType.OUT),
        8: Pin("6Y", PinType.OUT),
        9: Pin("6A", PinType.IN),
        10: Pin("5Y", PinType.OUT),
        11: Pin("5A", PinType.IN),
        12: Pin("4Y", PinType.OUT),
        13: Pin("4A", PinType.IN),
    }

    tests = [
        TestLogic("Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            body=[[x, ~x] for x in BV.range(0, 2**6)]
        )
    ]
