from binvec import BV
from prototypes import (PackageDIP24, Pin, Test)

class Part74181(PackageDIP24):
    name = "74181"
    desc = "Arithmetic logic units/function generators"
    pin_cfg = {
        1: Pin("B0", Pin.IN),
        2: Pin("A0", Pin.IN),
        3: Pin("S3", Pin.IN),
        4: Pin("S2", Pin.IN),
        5: Pin("S1", Pin.IN),
        6: Pin("S0", Pin.IN),
        7: Pin("~Cn", Pin.IN),
        8: Pin("M", Pin.IN),
        9: Pin("F0", Pin.OUT),
        10: Pin("F1", Pin.OUT),
        11: Pin("F2", Pin.OUT),
        13: Pin("F3", Pin.OUT),
        14: Pin("A=B", Pin.OC),  # A=B is really (F0 & F1 & F2 & F3)
        15: Pin("X", Pin.OUT),
        16: Pin("~Cn+4", Pin.OUT),
        17: Pin("Y", Pin.OUT),
        18: Pin("B3", Pin.IN),
        19: Pin("A3", Pin.IN),
        20: Pin("B2", Pin.IN),
        21: Pin("A2", Pin.IN),
        22: Pin("B1", Pin.IN),
        23: Pin("A1", Pin.IN),
    }

    missing_tests = "outputs G, P are not tested"

    # ------------------------------------------------------------------------
    def logic_test_gen(s, name, fun):
        # test vectors in [[inputs], [outputs]] order: [[1, s3-0, a3-0, b3-0], [f3-0, a=b]]
        body = lambda: [
            [
                [1, *BV.int(s, 4), *a, *b],
                [*fun(a, b), fun(a, b) == [1, 1, 1, 1]]
            ]
            for a in BV.range(0, 16)
            for b in BV.range(0, 16)
        ]

        return Test(name, Test.COMB,
            inputs=[8,  3, 4, 5, 6,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9, 14],
            loops=32,
            body=body,
        )

    # ------------------------------------------------------------------------
    def arith_test_gen(s, name, fun):
        # test vectors in [[inputs], [outputs]] order: [[0, s3-0, cin, a3-0, b3-0], [f3-0, cout, a=b]]
        body = lambda: [
            [
                [0, *BV.int(s, 4), *~c, *a, *b],
                [*(fun(a, b) + c), not (fun(a, b) + c).carry, fun(a, b) + c == [1, 1, 1, 1]]
            ]
            for a in BV.range(0, 16)
            for b in BV.range(0, 16)
            for c in BV.range(0, 2)
        ]
        return Test(name, Test.COMB,
            inputs=[8,  3, 4, 5, 6,  7,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9, 16, 14],
            loops=32,
            body=body
        )

    tests = [
        logic_test_gen(0, "Logic: F = ~A", lambda a, b: ~a),
        logic_test_gen(1, "Logic: F = ~(A|B)", lambda a, b: ~(a | b)),
        logic_test_gen(2, "Logic: F = ~A&B", lambda a, b: ~a & b),
        logic_test_gen(3, "Logic: F = 0", lambda a, b: BV.int(0, 4)),
        logic_test_gen(4, "Logic: F = ~(A&B)", lambda a, b: ~(a & b)),
        logic_test_gen(5, "Logic: F = ~B", lambda a, b: ~b),
        logic_test_gen(6, "Logic: F = A^B", lambda a, b: a ^ b),
        logic_test_gen(7, "Logic: F = A&~B", lambda a, b: a & ~b),
        logic_test_gen(8, "Logic: F = ~A|B", lambda a, b: ~a | b),
        logic_test_gen(9, "Logic: F = ~(A^B)", lambda a, b: ~(a ^ b)),
        logic_test_gen(10, "Logic: F = B", lambda a, b: b),
        logic_test_gen(11, "Logic: F = A&B", lambda a, b: a & b),
        logic_test_gen(12, "Logic: F = 1", lambda a, b: BV.int(0xf, 4)),  # F = 1 means all 1s
        logic_test_gen(13, "Logic: F = A|~B", lambda a, b: a | ~b),
        logic_test_gen(14, "Logic: F = A|B", lambda a, b: a | b),
        logic_test_gen(15, "Logic: F = A", lambda a, b: a),
        arith_test_gen(0, "Arithmetic: F = A", lambda a, b: a),
        arith_test_gen(1, "Arithmetic: F = A|B", lambda a, b: a | b),
        arith_test_gen(2, "Arithmetic: F = A|~B", lambda a, b: a | ~b),
        arith_test_gen(3, "Arithmetic: F = -1", lambda a, b: BV.int(15, 4)),
        arith_test_gen(4, "Arithmetic: F = A+(A&~B)", lambda a, b: a + (a & ~b)),
        arith_test_gen(5, "Arithmetic: F = (A|B)+(A&~B)", lambda a, b: (a | b) + (a & ~b)),
        arith_test_gen(6, "Arithmetic: F = A-B-1", lambda a, b: a + ~b),
        arith_test_gen(7, "Arithmetic: F = A&~B-1", lambda a, b: (a & ~b) + 15),
        arith_test_gen(8, "Arithmetic: F = A+(A&B)", lambda a, b: a + (a & b)),
        arith_test_gen(9, "Arithmetic: F = A+B", lambda a, b: a + b),
        arith_test_gen(10, "Arithmetic: F = (A|~B)+(A&B)", lambda a, b: (a | ~b) + (a & b)),
        arith_test_gen(11, "Arithmetic: F = (A&B)-1", lambda a, b: (a & b) + 15),
        arith_test_gen(12, "Arithmetic: F = A+A", lambda a, b: a + a),
        arith_test_gen(13, "Arithmetic: F = (A|B)+A", lambda a, b: (a | b) + a),
        arith_test_gen(14, "Arithmetic: F = (A|~B)+A", lambda a, b: (a | ~b) + a),
        arith_test_gen(15, "Arithmetic: F = A-1", lambda a, b: a + 15),
        # TODO: G, P (X, Y)
    ]
