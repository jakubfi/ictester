from prototypes import (PackageDIP16, Pin, Test)

class Part74194(PackageDIP16):
    name = "74194"
    desc = "4-bit bidirectional universal shift register"
    pin_cfg = {
        1: Pin("~CLR", Pin.IN),
        2: Pin("SR SER", Pin.IN),
        3: Pin("A", Pin.IN),
        4: Pin("B", Pin.IN),
        5: Pin("C", Pin.IN),
        6: Pin("D", Pin.IN),
        7: Pin("SL SER", Pin.IN),
        9: Pin("S0", Pin.IN),
        10: Pin("S1", Pin.IN),
        11: Pin("CLK", Pin.IN),
        12: Pin("QD", Pin.OUT),
        13: Pin("QC", Pin.OUT),
        14: Pin("QB", Pin.OUT),
        15: Pin("QA", Pin.OUT),
    }

    test_load = Test(
        name="Load",
        inputs=[1,  10, 9,  11,  7, 2,  3, 4, 5, 6],
        outputs=[15, 14, 13, 12],
        ttype=Test.SEQ,
        body=[
            # load 1's
            [[1,  1, 1,  '+',  0, 0,  1, 1, 1, 1], [1, 1, 1, 1]],
            # output current
            [[1,  0, 0,  '+',  0, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            # load 0's
            [[1,  1, 1,  '+',  1, 1,  0, 0, 0, 0], [0, 0, 0, 0]],
            # output current
            [[1,  0, 0,  '+',  1, 1,  1, 1, 1, 1], [0, 0, 0, 0]],

        ]
    )
    test_shright = Test(
        name="Shift right",
        inputs=[1,  10, 9,  11,  7, 2,  3, 4, 5, 6],
        outputs=[15, 14, 13, 12],
        ttype=Test.SEQ,
        body=[
            # shift right, insert 1's
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0], [1, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0], [1, 1, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0], [1, 1, 1, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0], [1, 1, 1, 1]],
            # shift right, insert 0's
            [[1,  0, 1,  '+',  1, 0,  1, 1, 1, 1], [0, 1, 1, 1]],
            [[1,  0, 1,  '+',  1, 0,  1, 1, 1, 1], [0, 0, 1, 1]],
            [[1,  0, 1,  '+',  1, 0,  1, 1, 1, 1], [0, 0, 0, 1]],
            [[1,  0, 1,  '+',  1, 0,  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )
    test_shleft = Test(
        name="Shift left",
        inputs=[1,  10, 9,  11,  7, 2,  3, 4, 5, 6],
        outputs=[15, 14, 13, 12],
        ttype=Test.SEQ,
        body=[
            # shift left, insert 1's
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0], [0, 0, 0, 1]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0], [0, 0, 1, 1]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0], [0, 1, 1, 1]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            # shift left, insert 0's
            [[1,  1, 0,  '+',  0, 1,  1, 1, 1, 1], [1, 1, 1, 0]],
            [[1,  1, 0,  '+',  0, 1,  1, 1, 1, 1], [1, 1, 0, 0]],
            [[1,  1, 0,  '+',  0, 1,  1, 1, 1, 1], [1, 0, 0, 0]],
            [[1,  1, 0,  '+',  0, 1,  1, 1, 1, 1], [0, 0, 0, 0]],

        ]
    )
    test_clear = Test(
        name="Clear",
        inputs=[1,  10, 9,  11,  7, 2,  3, 4, 5, 6],
        outputs=[15, 14, 13, 12],
        ttype=Test.SEQ,
        body=[
            # load 1's
            [[1,  1, 1,  '+',  0, 0,  1, 1, 1, 1], [1, 1, 1, 1]],
            # clear
            [[0,  1, 1,  '+',  1, 1,  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )

    tests = [test_load, test_shright, test_shleft, test_clear]
