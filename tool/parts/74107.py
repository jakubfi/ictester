from prototypes import (PackageDIP14, Pin, Test)

class Part74107(PackageDIP14):
    name = "74107"
    desc = "Dual J-K flip-flops with clear"
    pin_cfg = {
        1: Pin("1J", Pin.IN),
        2: Pin("~1Q", Pin.OUT),
        3: Pin("1Q", Pin.OUT),
        4: Pin("1K", Pin.IN),
        5: Pin("2Q", Pin.OUT),
        6: Pin("~2Q", Pin.OUT),
        8: Pin("2J", Pin.IN),
        9: Pin("2CLK", Pin.IN),
        10: Pin("~2CLR", Pin.IN),
        11: Pin("2K", Pin.IN),
        12: Pin("1CLK", Pin.IN),
        13: Pin("~1CLR", Pin.IN),
    }
    test_all = Test(
        name="Complete logic",
        inputs=[1, 4, 12, 13,  8, 11, 9, 10],
        outputs=[3, 2,  5, 6],
        ttype=Test.SEQ,
        body=[
            # reset
            [[1, 1, '-', 0,  1, 1, '-', 0], [0, 1,  0, 1]],
            # J
            [[1, 0, '-', 1,  1, 0, '-', 1], [1, 0,  1, 0]],
            # hold
            [[0, 0, '-', 1,  0, 0, '-', 1], [1, 0,  1, 0]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [0, 1,  0, 1]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [1, 0,  1, 0]],
            # K
            [[0, 1, '-', 1,  0, 1, '-', 1], [0, 1,  0, 1]],
            # toggle
            [[1, 1, '-', 1,  1, 1, '-', 1], [1, 0,  1, 0]],
        ]
    )
    tests = [test_all]