from collections import namedtuple
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
        14: Pin("A=B", Pin.OC),
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

    # ------------------------------------------------------------------------
    def logic_test_gen(s, name, fun):
        Vector = namedtuple('Vector', ['a', 'b', 'f'])

        # raw, numerical test data
        data = [
            Vector(a, b, fun(a, b))
            for a in range(0, 16)
            for b in range(0, 16)
        ]

        # test vectors in [[inputs], [outputs]] order:
        # [[1, s3, s2, s1, s0,  a3, a2, a1, a1,  b3, b2, b1, b0], [f3, f2, f1, f0]]
        body = [
            [
                [1] + Test.bin2vec(s, 4) + Test.bin2vec(v.a, 4) + Test.bin2vec(v.b, 4),
                Test.bin2vec(v.f, 4) + [int(v.f & 0b1111 == 0b1111)]
            ]
            for v in data
        ]

        return Test(
            name=name,
            inputs=[8,  3, 4, 5, 6,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9, 14],
            ttype=Test.COMB,
            loops=32,
            body=body,
        )

    # ------------------------------------------------------------------------
    def arith_test_gen(s, name, fun):
        Vector = namedtuple('Vector', ['a', 'b', 'c', 'f'])

        # raw, numerical test data
        data = [
            Vector(a, b, c, fun(a, b) + (not c))
            for a in range(0, 16)
            for b in range(0, 16)
            for c in range(0, 2)
        ]

        # test vectors in [[inputs], [outputs]] order:
        # [[0, s3, s2, s1, s0,  cin,  a3, a2, a1, a1,  b3, b2, b1, b0], [f3, f2, f1, f0,  cout]]
        body = [
            [
                [0] + Test.bin2vec(s, 4) + [v.c] + Test.bin2vec(v.a, 4) + Test.bin2vec(v.b, 4),
                Test.bin2vec(v.f & 0b1111, 4) + [int(not v.f & 0b10000)] + [int(v.f & 0b1111 == 0b1111)]
            ]
            for v in data
        ]
        return Test(
            name=name,
            inputs=[8,  3, 4, 5, 6,  7,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9, 16, 14],
            ttype=Test.COMB,
            loops=32,
            body=body
        )
    missing_tests = "outputs G, P are not tested"
    tests = [
        logic_test_gen(0, "Logic: F = ~A", lambda a, b: ~a),
        logic_test_gen(1, "Logic: F = ~(A|B)", lambda a, b: ~(a | b)),
        logic_test_gen(2, "Logic: F = ~A&B", lambda a, b: ~a & b),
        logic_test_gen(3, "Logic: F = 0", lambda a, b: 0),
        logic_test_gen(4, "Logic: F = ~(A&B)", lambda a, b: ~(a & b)),
        logic_test_gen(5, "Logic: F = ~B", lambda a, b: ~b),
        logic_test_gen(6, "Logic: F = A^B", lambda a, b: a ^ b),
        logic_test_gen(7, "Logic: F = A&~B", lambda a, b: a & ~b),
        logic_test_gen(8, "Logic: F = ~A|B", lambda a, b: ~a | b),
        logic_test_gen(9, "Logic: F = ~(A^B)", lambda a, b: ~(a ^ b)),
        logic_test_gen(10, "Logic: F = B", lambda a, b: b),
        logic_test_gen(11, "Logic: F = A&B", lambda a, b: a & b),
        logic_test_gen(12, "Logic: F = 1", lambda a, b: 0xf),
        logic_test_gen(13, "Logic: F = A|~B", lambda a, b: a | ~b),
        logic_test_gen(14, "Logic: F = A|B", lambda a, b: a | b),
        logic_test_gen(15, "Logic: F = A", lambda a, b: a),
        arith_test_gen(0, "Arithmetic: F = A", lambda a, b: a),
        arith_test_gen(1, "Arithmetic: F = A|B", lambda a, b: a | b),
        arith_test_gen(2, "Arithmetic: F = A|~B", lambda a, b: a | (~b & 15)),
        arith_test_gen(3, "Arithmetic: F = -1", lambda a, b: 15),
        arith_test_gen(4, "Arithmetic: F = A+(A&~B)", lambda a, b: a + (a & (~b & 15))),
        arith_test_gen(5, "Arithmetic: F = (A|B)+(A&~B)", lambda a, b: (a | b) + (a & (~b & 15))),
        arith_test_gen(6, "Arithmetic: F = A-B-1", lambda a, b: (a - b) + 15),
        arith_test_gen(7, "Arithmetic: F = A&~B-1", lambda a, b: (a & (~b & 15)) + 15),
        arith_test_gen(8, "Arithmetic: F = A+(A&B)", lambda a, b: a + (a & b)),
        arith_test_gen(9, "Arithmetic: F = A+B", lambda a, b: a + b),
        arith_test_gen(10, "Arithmetic: F = (A|~B)+(A&B)", lambda a, b: (a | (~b & 15)) + (a & b)),
        arith_test_gen(11, "Arithmetic: F = (A&B)-1", lambda a, b: (a & b) + 15),
        arith_test_gen(12, "Arithmetic: F = A+A", lambda a, b: a + a),
        arith_test_gen(13, "Arithmetic: F = (A|B)+A", lambda a, b: (a | b) + a),
        arith_test_gen(14, "Arithmetic: F = (A|~B)+A", lambda a, b: (a | (~b & 15)) + a),
        arith_test_gen(15, "Arithmetic: F = A-1", lambda a, b: a + 15),
        # TODO: G, P (X, Y)
    ]
