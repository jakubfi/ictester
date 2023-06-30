from binvec import BV
from prototypes import (PackageDIP16, Pin, Test)

class Part74S405(PackageDIP16):
    name = "74S405"
    desc = "1-from-8 binary decoder"
    pin_cfg = {
        1: Pin("A0", Pin.IN),
        2: Pin("A1", Pin.IN),
        3: Pin("A2", Pin.IN),
        4: Pin("~E1", Pin.IN),
        5: Pin("~E2", Pin.IN),
        6: Pin("E3", Pin.IN),
        7: Pin("O7", Pin.OUT),
        9: Pin("O6", Pin.OUT),
        10: Pin("O5", Pin.OUT),
        11: Pin("O4", Pin.OUT),
        12: Pin("O3", Pin.OUT),
        13: Pin("O2", Pin.OUT),
        14: Pin("O1", Pin.OUT),
        15: Pin("O0", Pin.OUT),
    }

    default_inputs = [4, 5, 6,  3, 2, 1]
    default_outputs = [7, 9, 10, 11, 12, 13, 14, 15]

    test_select = Test("Select", Test.COMB, default_inputs, default_outputs,
        body=[[[0, 0, 1, *BV.int(i, 3)],  ~BV.bit(i, 8)] for i in range(0, 8)]
    )
    test_inhibit = Test("Inhibit (all comb.)", Test.COMB, default_inputs, default_outputs,
        body=[[[*BV.int(i, 3), 0, 0, 0],  8*[1]] for i in set(range(0, 8)) - {1}]
    )

    tests = [test_select, test_inhibit]
