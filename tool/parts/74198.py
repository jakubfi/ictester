from part import (PackageDIP24, Pin, PinType)
from test import TestLogic

class Part74198(PackageDIP24):
    name = "74198"
    desc = "8-bit shift registers"
    pin_cfg = {
        1: Pin("S0", PinType.IN),
        2: Pin("SR_SER", PinType.IN),
        3: Pin("A", PinType.IN),
        4: Pin("QA", PinType.OUT),
        5: Pin("B", PinType.IN),
        6: Pin("QB", PinType.OUT),
        7: Pin("C", PinType.IN),
        8: Pin("QC", PinType.OUT),
        9: Pin("D", PinType.IN),
        10: Pin("QD", PinType.OUT),
        11: Pin("CLK", PinType.IN),
        13: Pin("~CLR", PinType.IN),
        14: Pin("QE", PinType.OUT),
        15: Pin("E", PinType.IN),
        16: Pin("QF", PinType.OUT),
        17: Pin("F", PinType.IN),
        18: Pin("QG", PinType.OUT),
        19: Pin("G", PinType.IN),
        20: Pin("QH", PinType.OUT),
        21: Pin("H", PinType.IN),
        22: Pin("SL_SER", PinType.IN),
        23: Pin("S1", PinType.IN),
    }

    default_inputs = [13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21]
    default_outputs = [4, 6, 8, 10, 14, 16, 18, 20]

    # NOTE: mode controls (S0, S1) should be changed only while the clock is high
    # NOTE: shift/load is done on rising clock edge
    # NOTE: clock is inhibited whe S0 and S1 are low
    # NOTE: CLEAR is async

    test_load = TestLogic("Parallel load", default_inputs, default_outputs,
        body=[
            [[1,  1, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  1, 1,  '-',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )
    test_clear = TestLogic("Clear", default_inputs, default_outputs,
        body=[
            # load 1s
            [[1,  1, 1,  '-',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            # clear
            [[0,  1, 1,  1,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
        ]
    )
    test_rshift = TestLogic("Shift right", default_inputs, default_outputs,
        body=[
            # clear
            [[0,  1, 1,  1,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # rshift
            [[1,  0, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0]],
            [[1,  0, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 0]],
            [[1,  0, 1,  '-',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0]],
            [[1,  0, 1,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1]],
        ]
    )
    test_lshift = TestLogic("Shift left", default_inputs, default_outputs,
        body=[
            # clear
            [[0,  1, 1,  1,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # lshift
            [[1,  1, 0,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  1, 0,  '-',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1]],
            [[1,  1, 0,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0]],
            [[1,  1, 0,  '-',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1]],
            [[1,  1, 0,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0]],
            [[1,  1, 0,  '-',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1]],
            [[1,  1, 0,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0]],
            [[1,  1, 0,  '-',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1]],
            [[1,  1, 0,  '-',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0]],
        ]
    )
    test_clk_inhibit = TestLogic("Clock inhibit", default_inputs, default_outputs,
        body=[
            # clear
            [[0,  1, 1,  1,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # clock inhibit
            [[1,  0, 0,  '-',  1, 1,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # load 1s
            [[1,  1, 1,  '-',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            # clock inhibit
            [[1,  0, 0,  '-',  1, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )

    tests = [test_load, test_clear, test_rshift, test_lshift, test_clk_inhibit]
