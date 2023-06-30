from binvec import BV
from prototypes import (PackageDIP16, Pin, Test)

# like 74151, different pinout

class Part9312(PackageDIP16):
    name = "9312"
    desc = "One of Eight Line Data Selectors/Multiplexers"
    pin_cfg = {
        1: Pin("D0", Pin.IN),
        2: Pin("D1", Pin.IN),
        3: Pin("D2", Pin.IN),
        4: Pin("D3", Pin.IN),
        5: Pin("D4", Pin.IN),
        6: Pin("D5", Pin.IN),
        7: Pin("D6", Pin.IN),
        9: Pin("D7", Pin.IN),
        10: Pin("~G", Pin.IN),
        11: Pin("A", Pin.IN),
        12: Pin("B", Pin.IN),
        13: Pin("C", Pin.IN),
        14: Pin("W", Pin.OUT),
        15: Pin("Y", Pin.OUT),
    }

    default_inputs = [9, 7, 6, 5, 4, 3, 2, 1,  13, 12, 11,  10]
    default_outputs = [15, 14]

    tests = [
        Test("Select 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 0],  [0, 1]] for addr in range(0, 8)]
        ),
        Test("Select 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 0],  [1, 0]] for addr in range(0, 8)]
        ),
        Test("Inhibit 0", Test.COMB, default_inputs, default_outputs,
            body=[[[*~BV.bit(addr, 8), *BV.int(addr, 3), 1],  [0, 1]] for addr in range(0, 8)]
        ),
        Test("Inhibit 1", Test.COMB, default_inputs, default_outputs,
            body=[[[*BV.bit(addr, 8), *BV.int(addr, 3), 1],  [0, 1]] for addr in range(0, 8)]
        )
    ]

