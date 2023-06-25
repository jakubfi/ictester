from prototypes import (PackageDIP14, Pin, Test)

class Part74LS54(PackageDIP14):
    name = "74LS54"
    desc = "4-wide And-Or-Invert gate"
    pin_cfg = {
        1: Pin("A", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("C", Pin.IN),
        4: Pin("D", Pin.IN),
        5: Pin("E", Pin.IN),
        6: Pin("Y", Pin.OUT),
        8: Pin("NC", Pin.NC),
        9: Pin("F", Pin.IN),
        10: Pin("G", Pin.IN),
        11: Pin("H", Pin.IN),
        12: Pin("I", Pin.IN),
        13: Pin("J", Pin.IN),
    }

    test_async = Test("Asynchronous operation", Test.COMB,
        inputs=[1, 2,  3, 4, 5,  9, 10, 11,  12, 13],
        outputs=[6],
        loops=256,
        body=[
            [
                i[0:10],
                [not ((i[0] & i[1]) | (i[2] & i[3] & i[4]) | (i[5] & i[6] & i[7]) | (i[8] & i[9]))]
            ] for i in Test.binary_combinator(10)
        ]
    )

    tests = [test_async]
