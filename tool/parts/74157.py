from prototypes import (PackageDIP16, Pin, Test)

class Part74157(PackageDIP16):
    name = "74157"
    desc = "Quad 2-line to 1-line data selectors/multiplexers"
    pin_cfg = {
        1: Pin("S", Pin.IN),
        2: Pin("A1", Pin.IN),
        3: Pin("B1", Pin.IN),
        4: Pin("Y1", Pin.OUT),
        5: Pin("A2", Pin.IN),
        6: Pin("B2", Pin.IN),
        7: Pin("Y2", Pin.OUT),
        9: Pin("Y3", Pin.OUT),
        10: Pin("B3", Pin.IN),
        11: Pin("A3", Pin.IN),
        12: Pin("Y4", Pin.OUT),
        13: Pin("B4", Pin.IN),
        14: Pin("A4", Pin.IN),
        15: Pin("G", Pin.IN),
    }
    test_all = Test(
        name="Complete logic",
        inputs=[15, 1,  2, 3,  5, 6,  11, 10,  14, 13],
        outputs=[4, 7, 9, 12],
        ttype=Test.COMB,
        body=[
            [[1, 0,  1, 1,  1, 1,  1, 1,  1, 1], [0, 0, 0, 0]],
            [[1, 1,  1, 1,  1, 1,  1, 1,  1, 1], [0, 0, 0, 0]],
            [[1, 0,  0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[1, 1,  0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],

            [[0, 0,  0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[0, 1,  0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[0, 0,  0, 1,  0, 1,  0, 1,  0, 1], [0, 0, 0, 0]],
            [[0, 1,  0, 1,  0, 1,  0, 1,  0, 1], [1, 1, 1, 1]],
            [[0, 0,  1, 0,  1, 0,  1, 0,  1, 0], [1, 1, 1, 1]],
            [[0, 1,  1, 0,  1, 0,  1, 0,  1, 0], [0, 0, 0, 0]],
            [[0, 0,  1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
            [[0, 1,  1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
        ]
    )
    tests = [test_all]
