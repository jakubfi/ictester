from functools import reduce
from prototypes import (PackageDIP14, Pin, Test)

def even(v):
    return reduce(lambda a, b: a==b, v)

class Part74180(PackageDIP14):
    name = "74180"
    desc = "9-bit odd/even parity generator/checker"
    pin_cfg = {
        1: Pin("G", Pin.IN),
        2: Pin("H", Pin.IN),
        3: Pin("EVEN", Pin.IN),
        4: Pin("ODD", Pin.IN),
        5: Pin("sumEVEN", Pin.OUT),
        6: Pin("sumODD", Pin.OUT),
        8: Pin("A", Pin.IN),
        9: Pin("B", Pin.IN),
        10: Pin("C", Pin.IN),
        11: Pin("D", Pin.IN),
        12: Pin("E", Pin.IN),
        13: Pin("F", Pin.IN),
    }

    default_inputs = [8, 9, 10, 11, 12, 13, 1, 2,  3, 4]
    default_outputs = [5, 6]

    test_valid_even = Test("Even upstream", Test.COMB, default_inputs, default_outputs,
        loops=64,
        body=[
            [data + [1, 0], [even(data), not even(data)]]
            for data in Test.binary_combinator(8)
        ]
    )
    test_valid_odd = Test("Odd upstream", Test.COMB, default_inputs, default_outputs,
        loops=64,
        body=[
            [data + [0, 1], [not even(data), even(data)]]
            for data in Test.binary_combinator(8)
        ]
    )
    test_invalid = Test("Invalid upstream", Test.COMB, default_inputs, default_outputs,
        loops=64,
        body=[
            [data + even_odd, list(map(lambda x: not x, even_odd))]
            for data in Test.binary_combinator(8)
            for even_odd in [[1, 1], [0, 0]]
        ]
    )

    tests = [test_valid_even, test_valid_odd, test_invalid]
