from binvec import BV
from prototypes import (PackageDIP16, Pin, Test)

class Part74151(PackageDIP16):
    name = "74151"
    desc = "Data selectors/multiplexers"
    pin_cfg = {
        1: Pin("D3", Pin.IN),
        2: Pin("D2", Pin.IN),
        3: Pin("D1", Pin.IN),
        4: Pin("D0", Pin.IN),
        5: Pin("Y", Pin.OUT),
        6: Pin("W", Pin.OUT),
        7: Pin("~G", Pin.IN),
        9: Pin("C", Pin.IN),
        10: Pin("B", Pin.IN),
        11: Pin("A", Pin.IN),
        12: Pin("D7", Pin.IN),
        13: Pin("D6", Pin.IN),
        14: Pin("D5", Pin.IN),
        15: Pin("D4", Pin.IN),
    }

    default_inputs = [12, 13, 14, 15, 1, 2, 3, 4,  9, 10, 11,  7]
    default_outputs = [5, 6]

    tests = [
        Test("Select 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 0],  [0, 1]] for addr in range(0, 8)]
        ),
        Test("Select 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 0],  [1, 0]] for addr in range(0, 8)]
        ),
        Test("Inhibit 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.int(0, 8), *addr, 1],  [0, 1]] for addr in BV.range(0, 8)]
        ),
        Test("Inhibit 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*~BV.int(0, 8), *addr, 1],  [0, 1]] for addr in BV.range(0, 8)]
        )
    ]
