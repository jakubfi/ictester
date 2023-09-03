from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74H87(PackageDIP14):
    name = "74H87"
    desc = "4-bit True/Complement, Zero/One Element"
    pin_cfg = {
        1: Pin("C", PinType.IN),
        2: Pin("A1", PinType.IN),
        3: Pin("Y1", PinType.OUT),
        4: Pin("NC", PinType.NC),
        5: Pin("A2", PinType.IN),
        6: Pin("Y2", PinType.OUT),
        8: Pin("B", PinType.IN),
        9: Pin("Y3", PinType.OUT),
        10: Pin("A3", PinType.IN),
        11: Pin("NC", PinType.NC),
        12: Pin("Y4", PinType.OUT),
        13: Pin("A4", PinType.IN),
    }

    default_inputs = [8, 1,  2, 5, 10, 13]
    default_outputs = [3, 6, 9, 12]

    test_true = Test("True", Test.LOGIC, default_inputs, default_outputs,
        body=[[[0, 1, *i], i] for i in BV.range(0, 16)]
    )
    test_complement = Test("Complement", Test.LOGIC, default_inputs, default_outputs,
        body=[[[0, 0, *i], ~i] for i in BV.range(0, 16)]
    )
    test_zero = Test("Zero", Test.LOGIC, default_inputs, default_outputs,
        body=[[[1, 1, *i], BV.int(0, 4)] for i in BV.range(0, 16)]
    )
    test_one = Test("One", Test.LOGIC, default_inputs, default_outputs,
        body=[[[1, 0, *i], ~BV.int(0, 4)] for i in BV.range(0, 16)]
    )

    tests = [test_true, test_complement, test_zero, test_one]
