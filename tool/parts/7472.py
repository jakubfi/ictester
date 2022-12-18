from prototypes import (PackageDIP14, Pin, Test)

class Part7472(PackageDIP14):
    name = "7472"
    desc = "And-gated J-K master-slave flip-flops with preset and clear"
    pin_cfg = {
        1: Pin("NC", Pin.NC),
        2: Pin("~CLR", Pin.IN),
        3: Pin("J1", Pin.IN),
        4: Pin("J2", Pin.IN),
        5: Pin("J3", Pin.IN),
        6: Pin("~Q", Pin.IN),
        8: Pin("Q", Pin.OUT),
        9: Pin("K1", Pin.OUT),
        10: Pin("K2", Pin.IN),
        11: Pin("K3", Pin.IN),
        12: Pin("CLK", Pin.IN),
        13: Pin("~PRE", Pin.IN),
    }

    default_inputs = [3, 4, 5,  9, 10, 11,  13, 2, 12]
    default_outputs = [8, 6]

    test_sync = Test("Load, clear, toogle, keep", Test.SEQ, default_inputs, default_outputs,
        body=[
            # load 1
            [[1, 1, 1,  0, 0, 0,  1, 1, '-'], [1, 0]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '-'], [1, 0]],
            # load 0
            [[0, 0, 0,  1, 1, 1,  1, 1, '-'], [0, 1]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '-'], [0, 1]],
            # toggle
            [[1, 1, 1,  1, 1, 1,  1, 1, '-'], [1, 0]],
            # keep
            [[0, 0, 0,  0, 0, 0,  1, 1, '-'], [1, 0]],
            # toggle
            [[1, 1, 1,  1, 1, 1,  1, 1, '-'], [0, 1]],
        ]
    )
    test_async = Test("Set, preset", Test.SEQ, default_inputs, default_outputs,
        body=[
            [[0, 0, 0,  1, 1, 1,  0, 1, '-'], [1, 0]],
            [[1, 1, 1,  0, 0, 0,  1, 0, '-'], [0, 1]],
            [[0, 0, 0,  1, 1, 1,  0, 1, '-'], [1, 0]],
            [[1, 1, 1,  0, 0, 0,  1, 0, '-'], [0, 1]],
            [[1, 1, 1,  1, 1, 1,  0, 1, '-'], [1, 0]],
            [[1, 1, 1,  1, 1, 1,  1, 0, '-'], [0, 1]],
            [[0, 0, 0,  0, 0, 0,  0, 1, '-'], [1, 0]],
            [[0, 0, 0,  0, 0, 0,  1, 0, '-'], [0, 1]],
        ]
    )
    test_and = Test("And input gates", Test.SEQ, default_inputs, default_outputs,
        body=[
            # try J=1 with not fully set K
            [[1, 1, 1,  0, 0, 0,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  0, 0, 1,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  0, 1, 0,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  0, 1, 1,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  1, 0, 0,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  1, 0, 1,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  1, 1, 0,  1, 1, '-'], [1, 0]],
            [[1, 1, 1,  1, 1, 1,  1, 1, '-'], [0, 1]],

            # try K=1 with not fully set J
            [[0, 0, 0,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[0, 0, 1,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[0, 1, 0,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[0, 1, 1,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[1, 0, 0,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[1, 0, 1,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[1, 1, 0,  1, 1, 1,  1, 1, '-'], [0, 1]],
            [[1, 1, 1,  1, 1, 1,  1, 1, '-'], [1, 0]],
        ]
    )

    tests = [test_sync, test_async, test_and]
