from binvec import BV
from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part74157(PackageDIP16):
    name = "74157"
    desc = "Quad 2-line to 1-line data selectors/multiplexers"
    pin_cfg = {
        1: Pin("S", PinType.IN),
        2: Pin("A1", PinType.IN),
        3: Pin("B1", PinType.IN),
        4: Pin("Y1", PinType.OUT),
        5: Pin("A2", PinType.IN),
        6: Pin("B2", PinType.IN),
        7: Pin("Y2", PinType.OUT),
        9: Pin("Y3", PinType.OUT),
        10: Pin("B3", PinType.IN),
        11: Pin("A3", PinType.IN),
        12: Pin("Y4", PinType.OUT),
        13: Pin("B4", PinType.IN),
        14: Pin("A4", PinType.IN),
        15: Pin("~G", PinType.IN),
    }

    default_inputs = [15, 1,  2, 3,  5, 6,  11, 10,  14, 13]
    default_outputs = [4, 7, 9, 12]

    test_inhibit = TestLogic("Inhibit", default_inputs, default_outputs,
        body=[
            [[1, addr, *(4*data)],  4*[0]]
            for addr in [0, 1]
            for data in BV.range(0, 4)
        ]
    )
    test_select = TestLogic("Select", default_inputs, default_outputs,
        body=[
            [[0, addr, *(4*data)],  4*[data[addr]]]
            for addr in [0, 1]
            for data in BV.range(0, 4)
        ]
    )

    tests = [test_select, test_inhibit]
