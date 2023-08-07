from binvec import BV
from prototypes import (PackageDIP20, Pin, Test)

class Part74S240(PackageDIP20):
    name = "74S240"
    desc = "Inverting Octal Buffers and Line Drivers With 3-State Outputs"
    pin_cfg = {
        # NOTE: outputs are really 3-state, but need more load to switch quickly, hence OC
        1: Pin("~1G", Pin.IN),
        2: Pin("1A1", Pin.IN),
        3: Pin("~2Y4", Pin.OC),
        4: Pin("1A2", Pin.IN),
        5: Pin("~2Y3", Pin.OC),
        6: Pin("1A3", Pin.IN),
        7: Pin("~2Y2", Pin.OC),
        8: Pin("1A4", Pin.IN),
        9: Pin("~2Y1", Pin.OC),
        11: Pin("2A1", Pin.IN),
        12: Pin("~1Y4", Pin.OC),
        13: Pin("2A2", Pin.IN),
        14: Pin("~1Y3", Pin.OC),
        15: Pin("2A3", Pin.IN),
        16: Pin("~1Y2", Pin.OC),
        17: Pin("2A4", Pin.IN),
        18: Pin("~1Y1", Pin.OC),
        19: Pin("~2G", Pin.IN),
    }

    default_inputs = [1,  2, 4, 6, 8,  19,  11, 13, 15, 17]
    default_outputs = [18, 16, 14, 12,  9, 7, 5, 3]

    tests = [
        Test("All logic", Test.COMB, default_inputs, default_outputs,
            body=[
                [[1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [1, 1, 1, 1,  1, 1, 1, 1]],
                [[1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [1, 1, 1, 1,  1, 1, 1, 1]],
                [[0,  1, 1, 1, 1,  0,  1, 1, 1, 1], [0, 0, 0, 0,  0, 0, 0, 0]],
                [[0,  0, 0, 0, 0,  0,  0, 0, 0, 0], [1, 1, 1, 1,  1, 1, 1, 1]],
            ]
        ),
    ]
