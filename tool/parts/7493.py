from prototypes import (PackageDIP14_vcc5, Pin, Test)

class Part7493(PackageDIP14_vcc5):
    name = "7493"
    desc = "4-bit binary counter"
    pin_cfg = {
        1: Pin("CKB", Pin.IN),
        2: Pin("R0(1)", Pin.IN),
        3: Pin("R0(2)", Pin.IN),
        4: Pin("NC", Pin.NC),
        6: Pin("NC", Pin.NC),
        7: Pin("NC", Pin.NC),
        8: Pin("QC", Pin.OUT),
        9: Pin("QB", Pin.OUT),
        11: Pin("QD", Pin.OUT),
        12: Pin("QA", Pin.OUT),
        13: Pin("NC", Pin.NC),
        14: Pin("CKA", Pin.IN),
    }

    test_count = Test("Count", Test.SEQ,
        inputs=[2, 3,  14, 1],
        outputs=[12, 9, 8, 11],
        body=[
            # reset
            [['-', '-',  0, 0], [0, 0, 0, 0]],
            # count CKA
            [[0, 0,  '-', 0], [1, 0, 0, 0]],
            [[0, 0,  '-', 0], [0, 0, 0, 0]],
            [[0, 0,  '-', 0], [1, 0, 0, 0]],
            # reset
            [['-', '-',  0, 0], [0, 0, 0, 0]],
            # count CKB
            [[0, 0,  0, '-'], [0, 1, 0, 0]],
            [[0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, '-'], [0, 1, 1, 0]],
            [[0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, '-'], [0, 1, 0, 1]],
            [[0, 0,  0, '-'], [0, 0, 1, 1]],
            [[0, 0,  0, '-'], [0, 1, 1, 1]],
            [[0, 0,  0, '-'], [0, 0, 0, 0]],
            # count CKB again to fill all bits with 1s
            [[0, 0,  0, '-'], [0, 1, 0, 0]],
            [[0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, '-'], [0, 1, 1, 0]],
            [[0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, '-'], [0, 1, 0, 1]],
            [[0, 0,  0, '-'], [0, 0, 1, 1]],
            [[0, 0,  0, '-'], [0, 1, 1, 1]],
            # no reset
            [[0, '-',  0, 0], [0, 1, 1, 1]],
            [['-', 0,  0, 0], [0, 1, 1, 1]],
        ]
    )

    tests = [test_count]
