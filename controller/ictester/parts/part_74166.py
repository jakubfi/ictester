from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part74166(PackageDIP16):
    name = "74166"
    desc = "Parallel-load 8-bit shift register"
    pin_cfg = {
        1: Pin("SER", PinType.IN),
        2: Pin("A", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("C", PinType.IN),
        5: Pin("D", PinType.IN),
        6: Pin("CLK_INH", PinType.IN),
        7: Pin("CLK", PinType.IN),
        9: Pin("~CLR", PinType.IN),
        10: Pin("E", PinType.IN),
        11: Pin("F", PinType.IN),
        12: Pin("G", PinType.IN),
        13: Pin("QH", PinType.OUT),
        14: Pin("H", PinType.IN),
        15: Pin("SH/~LD", PinType.IN),
    }

    # NOTE: clocked on rising edge
    # NOTE: clock inhibit should be changed on clock high
    # NOTE: clear overrides all inputs, including clock

    default_inputs = [9, 15,  6, 7,  1,  2, 3, 4, 5, 10, 11, 12, 14]
    default_outputs = [13]

    test_shift = TestLogic("Load, Shift", default_inputs, default_outputs,
        body=[
            # load all 1s
            [[1, 0,  0, '/',  0,  1, 1, 1, 1, 1, 1, 1, 1], [1]],
            # shift in 0s
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1,  0, '/',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # shift in 1s
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
        ]
    )
    test_clear = TestLogic("Load, Clear", default_inputs, default_outputs,
        body=[
            # load
            [[1, 0,  0, '/',  0,  1, 1, 1, 1, 1, 1, 1, 1], [1]],
            # clear
            [[0, 0,  0,  0,   0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # shift in 1s, shift out all 0s until last 1
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1,  0, '/',  1,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
        ]
    )
    test_inhibit_load = TestLogic("Clear, Inhibit Load", default_inputs, default_outputs,
        body=[
            # clear (+pull clock and clock inhibit high)
            [[0, 0,  1, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # inhibited loads
            [[1, 0,  1, '/',  0,  1, 1, 1, 1, 1, 1, 1, 1], [0]],
            [[1, 0,  1, '/',  0,  1, 1, 1, 1, 1, 1, 1, 1], [0]],
        ]
    )
    test_inhibit_shift = TestLogic("Clear, Inhibit Shift", default_inputs, default_outputs,
        body=[
            # clear (+pull clock and clock inhibit high)
            [[0, 0,  1, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # inhibited shift
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '/', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
        ]
    )

    tests = [test_shift, test_clear, test_inhibit_load, test_inhibit_shift]
