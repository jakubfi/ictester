from binvec import BV
from part import (PackageDIP14, Pin, PinType)
from test import TestLogic

class Part7401(PackageDIP14):
    name = "7401"
    desc = "Quad 2-input positive-NAND gates with open-collector outputs"
    pin_cfg = {
        1: Pin("1Y", PinType.OC),
        2: Pin("1A", PinType.IN),
        3: Pin("1B", PinType.IN),
        4: Pin("2Y", PinType.OC),
        5: Pin("2A", PinType.IN),
        6: Pin("2B", PinType.IN),
        8: Pin("3A", PinType.IN),
        9: Pin("3B", PinType.IN),
        10: Pin("3Y", PinType.OC),
        11: Pin("4A", PinType.IN),
        12: Pin("4B", PinType.IN),
        13: Pin("4Y", PinType.OC),
    }

    tests = [
        TestLogic("Complete logic",
            read_delay_us=0.6,
            inputs=[2, 3,  5, 6,  8, 9,  11, 12],
            outputs=[1, 4, 10, 13],
            body=[
                [[*g1, *g2, *g3, *g4], [not g1.vand(), not g2.vand(), not g3.vand(), not g4.vand()]]
                for g1 in BV.range(0, 2**2)
                for g2 in BV.range(0, 2**2)
                for g3 in BV.range(0, 2**2)
                for g4 in BV.range(0, 2**2)
            ]
        )
    ]

