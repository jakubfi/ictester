from prototypes import (PackageDIP14, Pin, Test)

class Part7495(PackageDIP14):
    name = "7495"
    desc = "4-bit parallel-access shift registers"
    pin_cfg = {
        1: Pin("SER", Pin.IN),
        2: Pin("A", Pin.IN),
        3: Pin("B", Pin.IN),
        4: Pin("C", Pin.IN),
        5: Pin("D", Pin.IN),
        6: Pin("MODE", Pin.IN),
        8: Pin("CLK2", Pin.IN),
        9: Pin("CLK1", Pin.IN),
        10: Pin("QD", Pin.OUT),
        11: Pin("QC", Pin.OUT),
        12: Pin("QB", Pin.OUT),
        13: Pin("QA", Pin.OUT),
    }
    test_load = Test(
        name="Parallel load",
        inputs=[6, 8, 9, 1, 2, 3, 4, 5],
        outputs=[13, 12, 11, 10],
        ttype=Test.SEQ,
        body=[
            [[1, '-', 0, 0, 1, 1, 1, 1], [1, 1, 1, 1]],
            [[1, '-', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )
    test_rshift = Test(
        name="Right Shift",
        inputs=[6, 8, 9, 1, 2, 3, 4, 5],
        outputs=[13, 12, 11, 10],
        ttype=Test.SEQ,
        body=[
            # set known starting value
            [[1, '-', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            # test shift
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 0]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 1]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )
    tests = [test_load, test_rshift]