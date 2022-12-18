from prototypes import (PackageDIP14_vcc5, Pin, Test)

class Part7490(PackageDIP14_vcc5):
    name = "7490"
    desc = "Decade counter"
    pin_cfg = {
        1: Pin("CKB", Pin.IN),
        2: Pin("R0(1)", Pin.IN),
        3: Pin("R0(2)", Pin.IN),
        4: Pin("NC", Pin.NC),
        6: Pin("R9-1", Pin.IN),
        7: Pin("R9-2", Pin.IN),
        8: Pin("QC", Pin.OUT),
        9: Pin("QB", Pin.OUT),
        11: Pin("QD", Pin.OUT),
        12: Pin("QA", Pin.OUT),
        13: Pin("NC", Pin.NC),
        14: Pin("CKA", Pin.IN),
    }

    default_inputs = [2, 3,  6, 7,  14, 1]
    default_outputs = [12, 11, 8, 9]

    test_resets = Test("Resets", Test.COMB, default_inputs, default_outputs,
        body=[
            # resets
            [[1, 1,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[1, 1,  0, 1,  0, 0], [0, 0, 0, 0]],
            [[0, 0,  1, 1,  0, 0], [1, 0, 0, 1]],
            [[0, 1,  1, 1,  0, 0], [1, 0, 0, 1]],
            [[1, 0,  1, 1,  0, 0], [1, 0, 0, 1]],
            [[1, 1,  1, 1,  0, 0], [1, 0, 0, 1]],
        ]
    )
    test_count_cka = Test("Count CKA", Test.SEQ, default_inputs, default_outputs,
        body=[
            # reset
            [[1, 1,  0, 0,  0, 0], [0, 0, 0, 0]],
            # count CKA
            [[0, 0,  0, 0,  '-', 0], [1, 0, 0, 0]],
            [[0, 0,  0, 0,  '-', 0], [0, 0, 0, 0]],
            [[0, 0,  0, 0,  '-', 0], [1, 0, 0, 0]],
        ]
    )
    test_count_ckb = Test("Count CKB", Test.SEQ, default_inputs, default_outputs,
        body=[
            #reset
            [[1, 1,  0, 0,  0, 0], [0, 0, 0, 0]],
            # count CKB
            [[0, 0,  0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, 0,  0, '-'], [0, 0, 1, 1]],
            [[0, 0,  0, 0,  0, '-'], [0, 1, 0, 0]],
            [[0, 0,  0, 0,  0, '-'], [0, 0, 0, 0]],
            # count CKB again to fill bits with 1s
            [[0, 0,  0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, 0,  0, '-'], [0, 0, 1, 1]],
        ]
    )

    tests = [test_resets, test_count_cka, test_count_ckb]
