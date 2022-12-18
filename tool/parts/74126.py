from prototypes import (PackageDIP14, Pin, Test)

class Part74126(PackageDIP14):
    name = "74126"
    desc = "Quarduple bus buffers with 3-state outputs"
    pin_cfg = {
        1: Pin("1G", Pin.IN),
        2: Pin("1A", Pin.IN),
        3: Pin("1Y", Pin.OC),
        4: Pin("2G", Pin.IN),
        5: Pin("2A", Pin.IN),
        6: Pin("2Y", Pin.OC),
        8: Pin("3Y", Pin.OC),
        9: Pin("3A", Pin.IN),
        10: Pin("3G", Pin.IN),
        11: Pin("4Y", Pin.OC),
        12: Pin("4A", Pin.IN),
        13: Pin("4G", Pin.IN),
    }

    test_all = Test("Complete logic", Test.COMB,
        inputs=[1, 2,  4, 5,  10, 9,  13, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [0, 0, 0, 0]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [1, 1, 1, 1]],
            [[0, 0,  0, 0,  0, 0,  0, 0], [1, 1, 1, 1]],
        ]
    )

    tests = [test_all]
