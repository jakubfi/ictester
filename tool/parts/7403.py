from binvec import BV
from part import (Pin, PinType, partimport)
from test import TestLogic

class Part7403(partimport("7400")):
    name = "7403"
    desc = "Quad 2-input positive-NAND gates with open-collector outputs"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("1Y", PinType.OC),
        4: Pin("2A", PinType.IN),
        5: Pin("2B", PinType.IN),
        6: Pin("2Y", PinType.OC),
        8: Pin("3Y", PinType.OC),
        9: Pin("3A", PinType.IN),
        10: Pin("3B", PinType.IN),
        11: Pin("4Y", PinType.OC),
        12: Pin("4A", PinType.IN),
        13: Pin("4B", PinType.IN),
    }

    tests = [
        TestLogic("Complete logic",
            read_delay_us=0.4,
            inputs=[1, 2, 4, 5, 9, 10, 12, 13],
            outputs=[3, 6, 8, 11],
            body=[
                [[*g1, *g2, *g3, *g4], [not g1.vand(), not g2.vand(), not g3.vand(), not g4.vand()]]
                for g1 in BV.range(0, 2**2)
                for g2 in BV.range(0, 2**2)
                for g3 in BV.range(0, 2**2)
                for g4 in BV.range(0, 2**2)
            ]
        )
    ]

