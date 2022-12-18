from prototypes import (PackageDIP16, Pin, Test)

class Part74166(PackageDIP16):
    name = "74166"
    desc = "Parallel-load 8-bit shift register"
    pin_cfg = {
        1: Pin("SER", Pin.IN),
        2: Pin("A", Pin.IN),
        3: Pin("B", Pin.IN),
        4: Pin("C", Pin.IN),
        5: Pin("D", Pin.IN),
        6: Pin("CLK INH", Pin.IN),
        7: Pin("CLK", Pin.OUT),
        9: Pin("~CLR", Pin.OUT),
        10: Pin("E", Pin.IN),
        11: Pin("F", Pin.IN),
        12: Pin("G", Pin.IN),
        13: Pin("QH", Pin.IN),
        14: Pin("H", Pin.IN),
        15: Pin("SH/~LD", Pin.IN),
    }

    default_inputs = [9, 15, 6, 7, 1, 2, 3, 4, 5, 10, 11, 12, 14]
    default_outputs = [13]

    test_shift = Test("Load, Shift", Test.SEQ, default_inputs, default_outputs,
        body=[
            # load
            [[1, 0, 0, '+', 0,  1, 1, 1, 1, 1, 1, 1, 1], [1]],
            # shift '0'
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            [[1, 1, 0, '+', 0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # shift '1'
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 0, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
        ]
    )
    test_clear = Test("Load, Clear", Test.COMB, default_inputs, default_outputs,
        body=[
            # load
            [[1, 0, 0, 1, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[1, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [1]],
            # clear
            [[0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
        ]
    )
    test_inhibit_load = Test("Clear, Inhibit Load", Test.COMB, default_inputs, default_outputs,
        body=[
            # clear
            [[0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # inhibited load
            [[1, 1, 1, 0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0]],
            [[1, 0, 1, 1, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0]],
            [[1, 0, 1, 0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0]],
        ]
    )
    test_inhibit_shift = Test("Clear, Inhibit Shift", Test.SEQ, default_inputs, default_outputs,
        body=[
            # clear
            [[0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            # inhibited shift
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 1, 1, '+', 1,  0, 0, 0, 0, 0, 0, 0, 0], [0]],
        ]
    )

    tests = [test_shift, test_clear, test_inhibit_load, test_inhibit_shift]
