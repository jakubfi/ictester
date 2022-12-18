from prototypes import (PackageDIP16, Pin, Test)

class Part74182(PackageDIP16):
    name = "74182"
    desc = "Look-ahead carry generator"
    pin_cfg = {
        1: Pin("~G1", Pin.IN),
        2: Pin("~P1", Pin.IN),
        3: Pin("~G0", Pin.IN),
        4: Pin("~P0", Pin.IN),
        5: Pin("~G3", Pin.IN),
        6: Pin("~P3", Pin.IN),
        7: Pin("~P", Pin.OUT),
        9: Pin("Cn+z", Pin.OUT),
        10: Pin("~G", Pin.OUT),
        11: Pin("Cn+y", Pin.OUT),
        12: Pin("Cn+x", Pin.OUT),
        13: Pin("Cn", Pin.IN),
        14: Pin("~G2", Pin.IN),
        15: Pin("~P2", Pin.IN),
    }

    test_g = Test("~G", Test.SEQ,
        inputs=[5, 14, 1, 3, 6, 15, 2],
        outputs=[10],
        loops=64,
        body=[
            [
                v, [0] if not v[0]
                or (not v[1] and not v[4])
                or (not v[2] and v[4:6] == [0, 0])
                or v[3:] == [0, 0, 0, 0]
                else [1]
            ]
            for v in Test.binary_combinator(7)
        ]
    )
    test_p = Test("~P", Test.SEQ,
        inputs=[2, 4, 6, 15],
        outputs=[7],
        loops=64,
        body=[
            [v, [0] if v == [0, 0, 0, 0] else [1]]
            for v in Test.binary_combinator(4)
        ]
    )
    test_cnx = Test("Cn+x", Test.SEQ,
        inputs=[3, 4, 13],
        outputs=[12],
        loops=64,
        body=[
            [v, [1] if not v[0] or v[1:3] == [0, 1] else [0]]
            for v in Test.binary_combinator(3)
        ]
    )
    test_cny = Test("Cn+y", Test.SEQ,
        inputs=[1, 3, 2, 4, 13],
        outputs=[11],
        loops=64,
        body=[
            [v, [1] if not v[0] or v[1:3] == [0, 0] or v[2:5] == [0, 0, 1] else [0]]
            for v in Test.binary_combinator(5)
        ]
    )
    test_cnz = Test("Cn+z", Test.SEQ,
        inputs=[14, 1, 3, 15, 2, 4, 13],
        outputs=[9],
        loops=64,
        body=[
            [v, [1] if not v[0] or (not v[1] and not v[3]) or v[2:5] == [0, 0, 0] or v[3:] == [0, 0, 0, 1] else [0]]
            for v in Test.binary_combinator(7)
        ]
    )

    tests = [test_g, test_p, test_cnx, test_cny, test_cnz]
