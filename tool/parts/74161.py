from prototypes import (PackageDIP16, Pin, Test)

class Part74161(PackageDIP16):
    name = "74161"
    desc = "Synchronous presettable 4-bit counter"
    pin_cfg = {
        1: Pin("~CLR", Pin.IN),
        2: Pin("CLK", Pin.IN),
        3: Pin("A", Pin.IN),
        4: Pin("B", Pin.IN),
        5: Pin("C", Pin.IN),
        6: Pin("D", Pin.IN),
        7: Pin("ENP", Pin.IN),
        9: Pin("~LOAD", Pin.IN),
        10: Pin("ENT", Pin.IN),
        11: Pin("QD", Pin.OUT),
        12: Pin("QC", Pin.OUT),
        13: Pin("QB", Pin.OUT),
        14: Pin("QA", Pin.OUT),
        15: Pin("RCO", Pin.OUT),
    }
    test_all = Test(
        name="Complete logic",
        inputs=[1, 9, 2,  10, 7,  6, 5, 4, 3],
        outputs=[11, 12, 13, 14,  15],
        ttype=Test.SEQ,
        body=[
            # NOTE: "enable" transitions done on clock high,
            # some chips are more sensitive to that
            # initial clear
            [['-', 1,   1,  0, 0,  0, 0, 0, 0], [0, 0, 0, 0,  0]],
            [[  1, 1,   1,  0, 0,  0, 0, 0, 0], [0, 0, 0, 0,  0]],
            # loads
            [[  1, 0,   1,  0, 0,  0, 0, 0, 0], [0, 0, 0, 0,  0]],
            [[  1, 0, '+',  0, 0,  0, 0, 0, 1], [0, 0, 0, 1,  0]],
            [[  1, 0, '+',  0, 0,  0, 0, 1, 0], [0, 0, 1, 0,  0]],
            [[  1, 0, '+',  0, 0,  0, 0, 1, 1], [0, 0, 1, 1,  0]],
            [[  1, 0, '+',  0, 0,  0, 1, 0, 0], [0, 1, 0, 0,  0]],
            [[  1, 0, '+',  0, 0,  0, 1, 0, 1], [0, 1, 0, 1,  0]],
            [[  1, 0, '+',  0, 0,  0, 1, 1, 0], [0, 1, 1, 0,  0]],
            [[  1, 0, '+',  0, 0,  0, 1, 1, 1], [0, 1, 1, 1,  0]],
            [[  1, 0, '+',  0, 0,  1, 0, 0, 0], [1, 0, 0, 0,  0]],
            [[  1, 0, '+',  0, 0,  1, 0, 0, 1], [1, 0, 0, 1,  0]],
            [[  1, 0, '+',  0, 0,  1, 0, 1, 0], [1, 0, 1, 0,  0]],
            [[  1, 0, '+',  0, 0,  1, 0, 1, 1], [1, 0, 1, 1,  0]],
            [[  1, 0, '+',  0, 0,  1, 1, 0, 0], [1, 1, 0, 0,  0]],
            [[  1, 0, '+',  0, 0,  1, 1, 0, 1], [1, 1, 0, 1,  0]],
            [[  1, 0, '+',  0, 0,  1, 1, 1, 0], [1, 1, 1, 0,  0]],
            [[  1, 0, '+',  0, 0,  1, 1, 1, 1], [1, 1, 1, 1,  0]],
            # disable load, enable count
            [[  1, 1,   1,  1, 1,  0, 0, 0, 0], [1, 1, 1, 1,  1]],
            # count
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 0, 0, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 0, 0, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 0, 1, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 0, 1, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 1, 0, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 1, 0, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 1, 1, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [0, 1, 1, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 0, 0, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 0, 0, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 0, 1, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 0, 1, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 1, 0, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 1, 0, 1,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 1, 1, 0,  0]],
            [[  1, 1, '+',  1, 1,  0, 0, 0, 0], [1, 1, 1, 1,  1]],
            # count inhibit
            [[  1, 1,   1,  0, 1,  0, 0, 0, 0], [1, 1, 1, 1,  0]],
            [[  1, 1,   0,  0, 1,  0, 0, 0, 0], [1, 1, 1, 1,  0]],
            [[  1, 1,   1,  0, 1,  0, 0, 0, 0], [1, 1, 1, 1,  0]],

            [[  1, 1,   1,  1, 0,  0, 0, 0, 0], [1, 1, 1, 1,  1]],
            [[  1, 1,   0,  1, 0,  0, 0, 0, 0], [1, 1, 1, 1,  1]],
            [[  1, 1,   1,  1, 0,  0, 0, 0, 0], [1, 1, 1, 1,  1]],

            [[  1, 1,   1,  0, 0,  0, 0, 0, 0], [1, 1, 1, 1,  0]],
            [[  1, 1,   0,  0, 0,  0, 0, 0, 0], [1, 1, 1, 1,  0]],
            [[  1, 1,   1,  0, 0,  0, 0, 0, 0], [1, 1, 1, 1,  0]],
        ]
    )
    tests = [test_all]