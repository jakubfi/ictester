from prototypes import (PackageDIP14, Pin, Test)

class Part7487(PackageDIP14):
    name = "7487"
    desc = "4-bit True/Complement, Zero/One Element"
    pin_cfg = {
        1: Pin("C", Pin.IN),
        2: Pin("A1", Pin.IN),
        3: Pin("Y1", Pin.OUT),
        4: Pin("NC", Pin.NC),
        5: Pin("A2", Pin.IN),
        6: Pin("Y2", Pin.OUT),
        8: Pin("B", Pin.IN),
        9: Pin("Y3", Pin.OUT),
        10: Pin("A3", Pin.IN),
        11: Pin("NC", Pin.NC),
        12: Pin("Y4", Pin.OUT),
        13: Pin("A4", Pin.IN),
    }
    test_all = Test(
        name="Complete logic",
        inputs=[8, 1,  2, 5, 10, 13],
        outputs=[3, 6, 9, 12],
        ttype=Test.COMB,
        body=[
            [[0, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            [[0, 0,  1, 1, 1, 1], [0, 0, 0, 0]],
            [[0, 1,  0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1,  1, 1, 1, 1], [1, 1, 1, 1]],
            [[1, 0,  0, 0, 0, 0], [1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1], [1, 1, 1, 1]],
            [[1, 1,  0, 0, 0, 0], [0, 0, 0, 0]],
            [[1, 1,  1, 1, 1, 1], [0, 0, 0, 0]],
        ]
    )
    tests = [test_all]