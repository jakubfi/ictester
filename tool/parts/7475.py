from prototypes import (PackageDIP16_vcc5, Pin, Test)

class Part7475(PackageDIP16_vcc5):
    name = "7475"
    desc = "4-bit bistable latches"
    pin_cfg = {
        1: Pin("~1Q", Pin.OUT),
        2: Pin("1D", Pin.IN),
        3: Pin("2D", Pin.IN),
        4: Pin("3C,4C", Pin.IN),
        6: Pin("3D", Pin.IN),
        7: Pin("4D", Pin.IN),
        8: Pin("~4Q", Pin.OUT),
        9: Pin("4Q", Pin.OUT),
        10: Pin("3Q", Pin.OUT),
        11: Pin("~3Q", Pin.OUT),
        13: Pin("1C,2C", Pin.IN),
        14: Pin("~2Q", Pin.OUT),
        15: Pin("2Q", Pin.OUT),
        16: Pin("1Q", Pin.OUT),
    }
    test_async = Test(
        name="Asynchronous operation",
        inputs=[2, 3, 13,  6, 7, 4],
        outputs=[16, 1,  15, 14,  10, 11,  9, 8],
        ttype=Test.COMB,
        body=[
            [[0, 0, 1,  0, 0, 1], [0, 1,  0, 1,  0, 1,  0, 1]],
            [[1, 1, 0,  1, 1, 0], [0, 1,  0, 1,  0, 1,  0, 1]],

            [[0, 1, 1,  0, 1, 1], [0, 1,  1, 0,  0, 1,  1, 0]],
            [[1, 0, 0,  1, 0, 0], [0, 1,  1, 0,  0, 1,  1, 0]],

            [[1, 0, 1,  1, 0, 1], [1, 0,  0, 1,  1, 0,  0, 1]],
            [[0, 1, 0,  0, 1, 0], [1, 0,  0, 1,  1, 0,  0, 1]],

            [[1, 1, 1,  1, 1, 1], [1, 0,  1, 0,  1, 0,  1, 0]],
            [[0, 0, 0,  0, 0, 0], [1, 0,  1, 0,  1, 0,  1, 0]],
        ]
    )
    tests = [test_async]
