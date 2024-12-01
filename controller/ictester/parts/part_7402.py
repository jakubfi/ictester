from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import TestLogic

class Part7402(PackageDIP14):
    name = "7402"
    desc = "Quad 2-input positive-NOR gates"
    pin_cfg = {
        1: Pin("1Y", PinType.OUT),
        2: Pin("1A", PinType.IN),
        3: Pin("1B", PinType.IN),
        4: Pin("2Y", PinType.OUT),
        5: Pin("2A", PinType.IN),
        6: Pin("2B", PinType.IN),
        8: Pin("3A", PinType.IN),
        9: Pin("3B", PinType.IN),
        10: Pin("3Y", PinType.OUT),
        11: Pin("4A", PinType.IN),
        12: Pin("4B", PinType.IN),
        13: Pin("4Y", PinType.OUT),
    }

    tests = [
        TestLogic("Complete logic",
            inputs=[2, 3, 5, 6, 8, 9, 11, 12],
            outputs=[1, 4, 10, 13],
            body=[
                [[*g1, *g2, *g3, *g4], [not g1.vor(), not g2.vor(), not g3.vor(), not g4.vor()]]
                for g1 in BV.range(0, 2**2)
                for g2 in BV.range(0, 2**2)
                for g3 in BV.range(0, 2**2)
                for g4 in BV.range(0, 2**2)
            ]
        )
    ]
