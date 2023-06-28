from binvec import BV
from prototypes import (PackageDIP24, Pin, Test)

class Part74150(PackageDIP24):
    name = "74150"
    desc = "Data selectors/multiplexers"
    pin_cfg = {
        1: Pin("E7", Pin.IN),
        2: Pin("E6", Pin.IN),
        3: Pin("E5", Pin.IN),
        4: Pin("E4", Pin.IN),
        5: Pin("E3", Pin.IN),
        6: Pin("E2", Pin.IN),
        7: Pin("E1", Pin.IN),
        8: Pin("E0", Pin.IN),
        9: Pin("~G", Pin.IN),
        10: Pin("W", Pin.OUT),
        11: Pin("D", Pin.IN),
        13: Pin("C", Pin.IN),
        14: Pin("B", Pin.IN),
        15: Pin("A", Pin.IN),
        16: Pin("E15", Pin.IN),
        17: Pin("E14", Pin.IN),
        18: Pin("E13", Pin.IN),
        19: Pin("E12", Pin.IN),
        20: Pin("E11", Pin.IN),
        21: Pin("E10", Pin.IN),
        22: Pin("E9", Pin.IN),
        23: Pin("E8", Pin.IN),
    }

    default_inputs = [11, 13, 14, 15,  9,  16, 17, 18, 19, 20, 21, 22, 23, 1, 2, 3, 4, 5, 6, 7, 8]
    default_outputs = [10]

    tests = [
        Test("Select 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 0, *~BV.bit(addr, 16)], [1]] for addr in range(0, 15)]
        ),
        Test("Select 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 0, *BV.bit(addr, 16)], [0]] for addr in range(0, 15)]
        ),
        Test("Inhibit 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 1, *BV.int(0, 16)], [1]] for addr in range(0, 15)]
        ),
        Test("Inhibit 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.int(addr, 4), 1, *~BV.int(0, 16)], [1]] for addr in range(0, 15)]
        ),
    ]
