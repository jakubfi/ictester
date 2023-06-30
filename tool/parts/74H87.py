from binvec import BV
from prototypes import (PackageDIP14, Pin, Test)

class Part74H87(PackageDIP14):
    name = "74H87"
    desc = "4-bit True/Complement, Zero/One Element"
    pin_cfg = {
        1: Pin("C", Pin.IN),
        2: Pin("A1", Pin.IN),
        3: Pin("Y1", Pin.OUT),
        4: Pin("NC", Pin.NC),
        5: Pin("A2", Pin.IN),
        6: Pin("Y2", Pin.OUT),
        8: Pin("B", Pin.IN),
        9: Pin("Y3", Pin.OUT),
        10: Pin("A3", Pin.IN),
        11: Pin("NC", Pin.NC),
        12: Pin("Y4", Pin.OUT),
        13: Pin("A4", Pin.IN),
    }

    default_inputs = [8, 1,  2, 5, 10, 13]
    default_outputs = [3, 6, 9, 12]

    test_true = Test("True", Test.COMB, default_inputs, default_outputs,
        body=[[[0, 1, *i], i] for i in BV.range(0, 16)]
    )
    test_complement = Test("Complement", Test.COMB, default_inputs, default_outputs,
        body=[[[0, 0, *i], ~i] for i in BV.range(0, 16)]
    )
    test_zero = Test("Zero", Test.COMB, default_inputs, default_outputs,
        body=[[[1, 1, *i], BV.int(0, 4)] for i in BV.range(0, 16)]
    )
    test_one = Test("One", Test.COMB, default_inputs, default_outputs,
        body=[[[1, 0, *i], ~BV.int(0, 4)] for i in BV.range(0, 16)]
    )

    tests = [test_true, test_complement, test_zero, test_one]
