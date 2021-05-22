import sys
import inspect
from functools import reduce
from collections import namedtuple
from prototypes import (Test, Pin, PartDIP14, PartDIP14x, PartDIP16, PartDIP16x, PartDIP16r, PartDIP24)


# ------------------------------------------------------------------------
# Translate integer value into a binary vector
# bin2vec(9, 7) -> [0, 0, 0, 1, 0, 0, 1]
def bin2vec(val, bitlen):
    return [
        (val >> (bitlen-pos-1)) & 1
        for pos in range(0, bitlen)
    ]


# ------------------------------------------------------------------------
# Get all bit combinations for given bit length
# binary_combinator(2) -> [[0, 0], [0, 1], [1, 0], [1, 1]]
def binary_combinator(bitlen):
    return [
        bin2vec(v, bitlen)
        for v in range(0, 2**bitlen)
    ]


# ------------------------------------------------------------------------
# Prepare test vectors for unit_cnt separate units with input_cnt inputs doing fun
# Units are tested inm parallel
# Four 3-input OR gates: binary_fun_gen(4, 3, lambda a, b: a|b)
def binary_fun_gen(unit_cnt, input_cnt, fun, inverted=False):
    return [
        [unit_cnt*v, unit_cnt*[reduce(fun, v) if not inverted else not reduce(fun, v)]]
        for v in binary_combinator(input_cnt)
    ]


# ------------------------------------------------------------------------
class Part7400(PartDIP14):
    name = "7400"
    desc = "Quad 2-input positive-NAND gates"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OUTPUT),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OUTPUT),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OUTPUT),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 4, 5, 10, 9, 13, 12],
            outputs=[3, 6, 8, 11],
            ttype=Test.COMB,
            body=binary_fun_gen(4, 2, lambda a, b: a & b, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7402(PartDIP14):
    name = "7402"
    desc = "Quad 2-input positive-NOR gates"
    pins = [
        Pin(1, "1Y", Pin.OUTPUT),
        Pin(2, "1A", Pin.INPUT),
        Pin(3, "1B", Pin.INPUT),
        Pin(4, "2Y", Pin.OUTPUT),
        Pin(5, "2A", Pin.INPUT),
        Pin(6, "2B", Pin.INPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3A", Pin.INPUT),
        Pin(9, "3B", Pin.INPUT),
        Pin(10, "3Y", Pin.OUTPUT),
        Pin(11, "4A", Pin.INPUT),
        Pin(12, "4B", Pin.INPUT),
        Pin(13, "4Y", Pin.OUTPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    tests = [
        Test(
            name="Complete logic",
            inputs=[2, 3, 5, 6, 8, 9, 11, 12],
            outputs=[1, 4, 10, 13],
            ttype=Test.COMB,
            body=binary_fun_gen(4, 2, lambda a, b: a | b, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7403(Part7400):
    name = "7403"
    desc = "Quad 2-input positive-NAND gates with open-collector outputs"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OC),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OC),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OC),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OC),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]


# ------------------------------------------------------------------------
class Part7404(PartDIP14):
    name = "7404"
    desc = "Hex inverters"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1Y", Pin.OUTPUT),
        Pin(3, "2A", Pin.INPUT),
        Pin(4, "2Y", Pin.OUTPUT),
        Pin(5, "3A", Pin.INPUT),
        Pin(6, "3Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "6Y", Pin.OUTPUT),
        Pin(9, "6A", Pin.INPUT),
        Pin(10, "5Y", Pin.OUTPUT),
        Pin(11, "5A", Pin.INPUT),
        Pin(12, "4Y", Pin.OUTPUT),
        Pin(13, "4A", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            ttype=Test.COMB,
            body=binary_fun_gen(6, 1, lambda a: a, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7405(Part7404):
    name = "7405"
    desc = "Hex inverters with open collector outputs"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1Y", Pin.OC),
        Pin(3, "2A", Pin.INPUT),
        Pin(4, "2Y", Pin.OC),
        Pin(5, "3A", Pin.INPUT),
        Pin(6, "3Y", Pin.OC),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "6Y", Pin.OC),
        Pin(9, "6A", Pin.INPUT),
        Pin(10, "5Y", Pin.OC),
        Pin(11, "5A", Pin.INPUT),
        Pin(12, "4Y", Pin.OC),
        Pin(13, "4A", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]


# ------------------------------------------------------------------------
class Part7406(Part7405):
    name = "7406"
    desc = "Hex inverter buffers / drivers with high-voltage outputs"


# ------------------------------------------------------------------------
class Part7407(Part7405):
    name = "7407"
    desc = "Hex Buffers/Drivers With Open-Collector High-Voltage Outputs"
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            ttype=Test.COMB,
            body=binary_fun_gen(6, 1, lambda a: a)
        )
    ]


# ------------------------------------------------------------------------
class Part7408(PartDIP14):
    name = "7408"
    desc = "Quad 2-input positive-AND gates"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OUTPUT),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OUTPUT),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OUTPUT),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 4, 5, 10, 9, 13, 12],
            outputs=[3, 6, 8, 11],
            ttype=Test.COMB,
            body=binary_fun_gen(4, 2, lambda a, b: a & b)
        )
    ]


# ------------------------------------------------------------------------
class Part7410(PartDIP14):
    name = "7410"
    desc = "Triple 3-input positive-NAND gates"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "2A", Pin.INPUT),
        Pin(4, "2B", Pin.INPUT),
        Pin(5, "2C", Pin.INPUT),
        Pin(6, "2Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OUTPUT),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "3C", Pin.INPUT),
        Pin(12, "1Y", Pin.OUTPUT),
        Pin(13, "1C", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]

    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 13, 3, 4, 5, 9, 10, 11],
            outputs=[12, 6, 8],
            ttype=Test.COMB,
            body=binary_fun_gen(3, 3, lambda a, b: a & b, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7412(Part7410):
    name = "7412"
    desc = "Triple 3-input positive-NAND gates with open-collector outputs"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "2A", Pin.INPUT),
        Pin(4, "2B", Pin.INPUT),
        Pin(5, "2C", Pin.INPUT),
        Pin(6, "2Y", Pin.OC),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OC),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "3C", Pin.INPUT),
        Pin(12, "1Y", Pin.OC),
        Pin(13, "1C", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]


# ------------------------------------------------------------------------
class Part7413(PartDIP14):
    name = "7413"
    desc = "Dual 4-input positive-NAND Schmitt triggers"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "NC", Pin.NC),
        Pin(4, "1C", Pin.INPUT),
        Pin(5, "1D", Pin.INPUT),
        Pin(6, "1Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "2Y", Pin.OUTPUT),
        Pin(9, "2A", Pin.INPUT),
        Pin(10, "2B", Pin.INPUT),
        Pin(11, "NC", Pin.NC),
        Pin(12, "2C", Pin.INPUT),
        Pin(13, "2D", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]

    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 4, 5, 13, 12, 10, 9],
            outputs=[6, 8],
            ttype=Test.COMB,
            body=binary_fun_gen(2, 4, lambda a, b: a & b, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7420(Part7413):
    name = "7420"
    desc = "Dual 4-input positive-NAND gates"


# ------------------------------------------------------------------------
class Part7430(PartDIP14):
    name = "7430"
    desc = "8-input positive-NAND gate"
    pins = [
        Pin(1, "A", Pin.INPUT),
        Pin(2, "B", Pin.INPUT),
        Pin(3, "C", Pin.INPUT),
        Pin(4, "D", Pin.INPUT),
        Pin(5, "E", Pin.INPUT),
        Pin(6, "F", Pin.INPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "Y", Pin.OUTPUT),
        Pin(9, "NC", Pin.NC),
        Pin(10, "NC", Pin.NC),
        Pin(11, "G", Pin.INPUT),
        Pin(12, "H", Pin.INPUT),
        Pin(13, "NC", Pin.NC),
        Pin(14, "VCC", Pin.POWER),
    ]

    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 3, 4, 5, 6, 11, 12],
            outputs=[8],
            ttype=Test.COMB,
            body=binary_fun_gen(1, 8, lambda a, b: a & b, inverted=True)
        )
    ]


# ------------------------------------------------------------------------
class Part7432(PartDIP14):
    name = "7432"
    desc = "Quad 2-input positive-OR gates"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OUTPUT),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OUTPUT),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OUTPUT),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 2, 4, 5, 10, 9, 13, 12],
            outputs=[3, 6, 8, 11],
            ttype=Test.COMB,
            body=binary_fun_gen(4, 2, lambda a, b: a | b)
        )
    ]


# ------------------------------------------------------------------------
class Part7437(Part7400):
    name = "7437"
    desc = "Quad 2-input positive-NAND buffers"


# ------------------------------------------------------------------------
class Part7438(Part7400):
    name = "7438"
    desc = "Quad 2-input positive-NAND buffers with open collector outputs"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OC),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OC),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OC),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OC),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]


# ------------------------------------------------------------------------
class Part7445(PartDIP16):
    name = "7445"
    desc = "BCD-to-decimal decoders/drivers"
    pins = [
        Pin(1, "0", Pin.OC),
        Pin(2, "1", Pin.OC),
        Pin(3, "2", Pin.OC),
        Pin(4, "3", Pin.OC),
        Pin(5, "4", Pin.OC),
        Pin(6, "5", Pin.OC),
        Pin(7, "6", Pin.OC),
        Pin(8, "GND", Pin.POWER),
        Pin(9, "7", Pin.OC),
        Pin(10, "8", Pin.OC),
        Pin(11, "9", Pin.OC),
        Pin(12, "D", Pin.INPUT),
        Pin(13, "C", Pin.INPUT),
        Pin(14, "B", Pin.INPUT),
        Pin(15, "A", Pin.INPUT),
        Pin(16, "VCC", Pin.POWER),
    ]
    test_async = Test(
        name="Asynchronous operation",
        inputs=[12, 13, 14, 15],
        outputs=[1, 2, 3, 4, 5, 6, 7, 9, 10, 11],
        ttype=Test.COMB,
        body=[
            [[0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 0, 1], [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 1, 0], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1]],
            [[0, 0, 1, 1], [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]],
            [[0, 1, 0, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]],
            [[0, 1, 0, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]],
            [[0, 1, 1, 0], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]],
            [[0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 1]],
            [[1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]],
            [[1, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
            [[1, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )
    tests = [test_async]


# ------------------------------------------------------------------------
class Part7474(PartDIP14):
    name = "7474"
    desc = "Dual D-type positive-edge-triggered flip-flops with preset and clear"
    pins = [
        Pin(1, "~1CLR", Pin.INPUT),
        Pin(2, "1D", Pin.INPUT),
        Pin(3, "1CLK", Pin.INPUT),
        Pin(4, "~1PRE", Pin.INPUT),
        Pin(5, "1Q", Pin.OUTPUT),
        Pin(6, "~1Q", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "~2Q", Pin.OUTPUT),
        Pin(9, "2Q", Pin.OUTPUT),
        Pin(10, "~2PRE", Pin.INPUT),
        Pin(11, "2CLK", Pin.INPUT),
        Pin(12, "2D", Pin.INPUT),
        Pin(13, "~2CLR", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    test_sync = Test(
        name="Synchronous operation",
        inputs=[1, 4, 2, 3, 13, 10, 12, 11],
        outputs=[5, 6, 9, 8],
        ttype=Test.SEQ,
        body=[
            [[1, 1, 0, '+',  1, 1, 0, '+'], [0, 1,  0, 1]],
            [[1, 1, 1, '+',  1, 1, 1, '+'], [1, 0,  1, 0]],
        ]
    )
    test_async = Test(
        name="Asynchronous operation",
        inputs=[1, 4, 2, 3, 13, 10, 12, 11],
        outputs=[5, 6, 9, 8],
        ttype=Test.COMB,
        body=[
            [[0, 1, 0, 0,  0, 1, 0, 0], [0, 1,  0, 1]],
            [[1, 0, 0, 0,  1, 0, 0, 0], [1, 0,  1, 0]],
        ]
    )
    tests = [test_sync, test_async]


# ------------------------------------------------------------------------
class Part7483(PartDIP16x):
    name = "7483"
    desc = "4-bit binary full adder with fast carry"
    pins = [
        Pin(1, "A4", Pin.INPUT),
        Pin(2, "S3", Pin.OUTPUT),
        Pin(3, "A3", Pin.INPUT),
        Pin(4, "B3", Pin.INPUT),
        Pin(5, "VCC", Pin.POWER),
        Pin(6, "S2", Pin.OUTPUT),
        Pin(7, "B2", Pin.INPUT),
        Pin(8, "A2", Pin.INPUT),
        Pin(9, "S1", Pin.OUTPUT),
        Pin(10, "A1", Pin.INPUT),
        Pin(11, "B1", Pin.INPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "C0", Pin.INPUT),
        Pin(14, "C4", Pin.OUTPUT),
        Pin(15, "S4", Pin.OUTPUT),
        Pin(16, "B4", Pin.INPUT),
    ]

    # ------------------------------------------------------------------------
    def add_test_gen():
        Vector = namedtuple('Vector', ['a', 'b', 'c', 'f'])

        # raw, numerical test data
        data = [
            Vector(a, b, c, a + b + c)
            for a in range(0, 16)
            for b in range(0, 16)
            for c in range(0, 2)
        ]

        # test vectors in [[inputs], [outputs]] order:
        # [[cin, a4, a3, a2, a1,  b4, b3, b2, b1], [f4, f3, f2, f1,  cout]]
        body = [
            [
                [v.c] + bin2vec(v.a, 4) + bin2vec(v.b, 4),
                bin2vec(v.f & 0b1111, 4) + [True if v.f & 0b10000 else False]
            ]
            for v in data
        ]
        return body

    test_all = Test(
        name="Complete logic",
        inputs=[13,  1, 3, 8, 10,  16, 4, 7, 11],
        outputs=[15, 2, 6, 9,  14],
        ttype=Test.COMB,
        body=add_test_gen()
    )
    tests = [test_all]


# ------------------------------------------------------------------------
class Part7486(PartDIP14):
    name = "7486"
    desc = "Quad 2-input exclusive-OR gates"
    pins = [
        Pin(1, "1A", Pin.INPUT),
        Pin(2, "1B", Pin.INPUT),
        Pin(3, "1Y", Pin.OUTPUT),
        Pin(4, "2A", Pin.INPUT),
        Pin(5, "2B", Pin.INPUT),
        Pin(6, "2Y", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "3Y", Pin.OUTPUT),
        Pin(9, "3A", Pin.INPUT),
        Pin(10, "3B", Pin.INPUT),
        Pin(11, "4Y", Pin.OUTPUT),
        Pin(12, "4A", Pin.INPUT),
        Pin(13, "4B", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    test_all = Test(
        name="Complete logic",
        inputs=[1, 2, 4, 5, 10, 9, 13, 12],
        outputs=[3, 6, 8, 11],
        ttype=Test.COMB,
        body=binary_fun_gen(4, 2, lambda a, b: a ^ b)
    )
    tests = [test_all]


# ------------------------------------------------------------------------
class Part7493(PartDIP14x):
    name = "7493"
    desc = "4-bit binar counter"
    pins = [
        Pin(1, "CKB", Pin.INPUT),
        Pin(2, "R0(1)", Pin.INPUT),
        Pin(3, "R0(2)", Pin.INPUT),
        Pin(4, "NC", Pin.NC),
        Pin(5, "VCC", Pin.POWER),
        Pin(6, "NC", Pin.NC),
        Pin(7, "NC", Pin.NC),
        Pin(8, "QC", Pin.OUTPUT),
        Pin(9, "QB", Pin.OUTPUT),
        Pin(10, "GND", Pin.POWER),
        Pin(11, "QD", Pin.OUTPUT),
        Pin(12, "QA", Pin.OUTPUT),
        Pin(13, "NC", Pin.NC),
        Pin(14, "CKA", Pin.INPUT),
    ]
    test_count = Test(
        name="Count",
        inputs=[2, 3,  14, 1],
        outputs=[12, 9, 8, 11],
        ttype=Test.SEQ,
        body=[
            # reset
            [['-', '-',  0, 0], [0, 0, 0, 0]],
            # count CKA
            [[0, 0,  '-', 0], [1, 0, 0, 0]],
            [[0, 0,  '-', 0], [0, 0, 0, 0]],
            [[0, 0,  '-', 0], [1, 0, 0, 0]],
            # reset
            [['-', '-',  0, 0], [0, 0, 0, 0]],
            # count CKB
            [[0, 0,  0, '-'], [0, 1, 0, 0]],
            [[0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, '-'], [0, 1, 1, 0]],
            [[0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, '-'], [0, 1, 0, 1]],
            [[0, 0,  0, '-'], [0, 0, 1, 1]],
            [[0, 0,  0, '-'], [0, 1, 1, 1]],
            [[0, 0,  0, '-'], [0, 0, 0, 0]],
            # count CKB again to fill all bits with 1s
            [[0, 0,  0, '-'], [0, 1, 0, 0]],
            [[0, 0,  0, '-'], [0, 0, 1, 0]],
            [[0, 0,  0, '-'], [0, 1, 1, 0]],
            [[0, 0,  0, '-'], [0, 0, 0, 1]],
            [[0, 0,  0, '-'], [0, 1, 0, 1]],
            [[0, 0,  0, '-'], [0, 0, 1, 1]],
            [[0, 0,  0, '-'], [0, 1, 1, 1]],
            # no reset
            [[0, '-',  0, 0], [0, 1, 1, 1]],
            [['-', 0,  0, 0], [0, 1, 1, 1]],
        ]
    )
    tests = [test_count]


# ------------------------------------------------------------------------
class Part7495(PartDIP14):
    name = "7495"
    desc = "4-bit parallel-access shift registers"
    pins = [
        Pin(1, "SER", Pin.INPUT),
        Pin(2, "A", Pin.INPUT),
        Pin(3, "B", Pin.INPUT),
        Pin(4, "C", Pin.INPUT),
        Pin(5, "D", Pin.INPUT),
        Pin(6, "MODE", Pin.INPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "CLK2", Pin.INPUT),
        Pin(9, "CLK1", Pin.INPUT),
        Pin(10, "QD", Pin.OUTPUT),
        Pin(11, "QC", Pin.OUTPUT),
        Pin(12, "QB", Pin.OUTPUT),
        Pin(13, "QA", Pin.OUTPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    test_load = Test(
        name="Parallel load",
        inputs=[6, 8, 9, 1, 2, 3, 4, 5],
        outputs=[13, 12, 11, 10],
        ttype=Test.SEQ,
        body=[
            [[1, '-', 0, 0, 1, 1, 1, 1], [1, 1, 1, 1]],
            [[1, '-', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )
    test_rshift = Test(
        name="Right Shift",
        inputs=[6, 8, 9, 1, 2, 3, 4, 5],
        outputs=[13, 12, 11, 10],
        ttype=Test.SEQ,
        body=[
            # set known starting value
            [[1, '-', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            # test shift
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 0]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '-', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 1, 0]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 1]],
            [[0, 0, '-', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )
    tests = [test_load, test_rshift]


# ------------------------------------------------------------------------
class Part7496(PartDIP16x):
    name = "7496"
    desc = "5-bit shift register"
    pins = [
        Pin(1, "CLK", Pin.INPUT),
        Pin(2, "A", Pin.INPUT),
        Pin(3, "B", Pin.INPUT),
        Pin(4, "C", Pin.INPUT),
        Pin(5, "VCC", Pin.POWER),
        Pin(6, "D", Pin.INPUT),
        Pin(7, "E", Pin.INPUT),
        Pin(8, "PRE", Pin.INPUT),
        Pin(9, "SER", Pin.INPUT),
        Pin(10, "QE", Pin.OUTPUT),
        Pin(11, "QD", Pin.OUTPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "QC", Pin.OUTPUT),
        Pin(14, "QB", Pin.OUTPUT),
        Pin(15, "QA", Pin.OUTPUT),
        Pin(16, "CLR", Pin.INPUT),
    ]

    test_preset = Test(
        name="Preset",
        inputs=[16, 8,  2, 3, 4, 6, 7,  1, 9],
        outputs=[15, 14, 13, 11, 10],
        ttype=Test.COMB,
        body=[
            # preset all 1
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            # clear
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset selective 1s
            [[1, 1,  0, 0, 0, 0, 1,  0, 0], [0, 0, 0, 0, 1]],
            [[1, 1,  0, 0, 0, 1, 0,  0, 0], [0, 0, 0, 1, 1]],
            [[1, 1,  0, 0, 1, 0, 0,  0, 0], [0, 0, 1, 1, 1]],
            [[1, 1,  0, 1, 0, 0, 0,  0, 0], [0, 1, 1, 1, 1]],
            [[1, 1,  1, 0, 0, 0, 0,  0, 0], [1, 1, 1, 1, 1]],
            # clear, preset known
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            [[1, 1,  0, 1, 0, 1, 0,  0, 0], [0, 1, 0, 1, 0]],
            # no action
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 1, 0, 1, 0]],
        ]
    )

    test_clear = Test(
        name="Clear",
        inputs=[16, 8,  2, 3, 4, 6, 7,  1, 9],
        outputs=[15, 14, 13, 11, 10],
        ttype=Test.COMB,
        body=[
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 1,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 0, 0]],
        ]
    )

    test_serial_in = Test(
        name="Serial in",
        inputs=[16, 8,  2, 3, 4, 6, 7,  1, 9],
        outputs=[15, 14, 13, 11, 10],
        ttype=Test.COMB,
        body=[
            # clear, preset known
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            [[1, 1,  1, 0, 1, 0, 1,  0, 0], [1, 0, 1, 0, 1]],
            # shift in 1s
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 0, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 0, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 0, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 1, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1, 1]],
            # shift in 0s
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 0, 0]],
        ]
    )

    tests = [
        test_preset,
        test_clear,
        test_serial_in,
    ]


# ------------------------------------------------------------------------
class Part74150(PartDIP24):
    name = "74150"
    desc = "Data selectors/multiplexers"
    pins = [
        Pin(1, "E7", Pin.INPUT),
        Pin(2, "E6", Pin.INPUT),
        Pin(3, "E5", Pin.INPUT),
        Pin(4, "E4", Pin.INPUT),
        Pin(5, "E3", Pin.INPUT),
        Pin(6, "E2", Pin.INPUT),
        Pin(7, "E1", Pin.INPUT),
        Pin(8, "E0", Pin.INPUT),
        Pin(9, "~G", Pin.INPUT),
        Pin(10, "W", Pin.OUTPUT),
        Pin(11, "D", Pin.INPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "C", Pin.INPUT),
        Pin(14, "B", Pin.INPUT),
        Pin(15, "A", Pin.INPUT),
        Pin(16, "E15", Pin.INPUT),
        Pin(17, "E14", Pin.INPUT),
        Pin(18, "E13", Pin.INPUT),
        Pin(19, "E12", Pin.INPUT),
        Pin(20, "E11", Pin.INPUT),
        Pin(21, "E10", Pin.INPUT),
        Pin(22, "E9", Pin.INPUT),
        Pin(23, "E8", Pin.INPUT),
        Pin(24, "VCC", Pin.POWER),
    ]
    test_all = Test(
        name="Complete logic",
        inputs=[11, 13, 14, 15,  9,  8, 7, 6, 5, 4, 3, 2, 1, 23, 22, 21, 20, 19, 18, 17, 16],
        outputs=[10],
        ttype=Test.COMB,
        body=[
            [[0, 0, 0, 0,  1,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1]],

            [[0, 0, 0, 0,  0,  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 0, 0, 1,  0,  0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 0, 1, 0,  0,  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 0, 1, 1,  0,  0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 1, 0, 0,  0,  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 1, 0, 1,  0,  0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 1, 1, 0,  0,  0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[0, 1, 1, 1,  0,  0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 0, 0, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0]],
            [[1, 0, 1, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0]],
            [[1, 0, 1, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0]],
            [[1, 1, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0]],
            [[1, 1, 0, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0]],
            [[1, 1, 1, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0]],
            [[1, 1, 1, 1,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0]],

            [[0, 0, 0, 0,  0,  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 0, 0, 1,  0,  1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 0, 1, 0,  0,  1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 0, 1, 1,  0,  1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 1, 0, 0,  0,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 1, 0, 1,  0,  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 1, 1, 0,  0,  1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[0, 1, 1, 1,  0,  1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[1, 0, 0, 0,  0,  1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1]],
            [[1, 0, 0, 1,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1]],
            [[1, 0, 1, 0,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1]],
            [[1, 0, 1, 1,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1]],
            [[1, 1, 0, 0,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], [1]],
            [[1, 1, 0, 1,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1], [1]],
            [[1, 1, 1, 0,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1]],
            [[1, 1, 1, 1,  0,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1]],
        ]
    )
    tests = [test_all]


# ------------------------------------------------------------------------
class Part74153(PartDIP16):
    name = "74153"
    desc = "Dual 4-line to 1-line data selectors/multiplexers"
    pins = [
        Pin(1, "~1G", Pin.INPUT),
        Pin(2, "B", Pin.INPUT),
        Pin(3, "1C3", Pin.INPUT),
        Pin(4, "1C2", Pin.INPUT),
        Pin(5, "1C1", Pin.INPUT),
        Pin(6, "1C0", Pin.INPUT),
        Pin(7, "1Y", Pin.OUTPUT),
        Pin(8, "GND", Pin.POWER),
        Pin(9, "2Y", Pin.OUTPUT),
        Pin(10, "2C0", Pin.INPUT),
        Pin(11, "2C1", Pin.INPUT),
        Pin(12, "2C2", Pin.INPUT),
        Pin(13, "2C3", Pin.INPUT),
        Pin(14, "A", Pin.INPUT),
        Pin(15, "~2G", Pin.INPUT),
        Pin(16, "VCC", Pin.POWER),
    ]
    test_all = Test(
        name="Complete logic",
        inputs=[2, 14, 1, 3, 4, 5, 6, 15, 13, 12, 11, 10],
        outputs=[7, 9],
        ttype=Test.COMB,
        body=[
            # output is always "0" when G is high
            [[0, 0,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[0, 1,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[1, 0,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[1, 1,  1,  0, 0, 0, 0,  1,  0, 0, 0, 0], [0, 0]],
            [[0, 0,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[0, 1,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[1, 0,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],
            [[1, 1,  1,  1, 1, 1, 1,  1,  1, 1, 1, 1], [0, 0]],

            # selection if G is low
            [[0, 0,  0,  1, 1, 1, 0,  0,  1, 1, 1, 0], [0, 0]],
            [[0, 1,  0,  1, 1, 0, 1,  0,  1, 1, 0, 1], [0, 0]],
            [[1, 0,  0,  1, 0, 1, 1,  0,  1, 0, 1, 1], [0, 0]],
            [[1, 1,  0,  0, 1, 1, 1,  0,  0, 1, 1, 1], [0, 0]],

            [[0, 0,  0,  0, 0, 0, 1,  0,  0, 0, 0, 1], [1, 1]],
            [[0, 1,  0,  0, 0, 1, 0,  0,  0, 0, 1, 0], [1, 1]],
            [[1, 0,  0,  0, 1, 0, 0,  0,  0, 1, 0, 0], [1, 1]],
            [[1, 1,  0,  1, 0, 0, 0,  0,  1, 0, 0, 0], [1, 1]],
        ]
    )
    tests = [test_all]


# ------------------------------------------------------------------------
class Part74181(PartDIP24):
    name = "74181"
    desc = "Arithmetic logic units/function generators"
    pins = [
        Pin(1, "B0", Pin.INPUT),
        Pin(2, "A0", Pin.INPUT),
        Pin(3, "S3", Pin.INPUT),
        Pin(4, "S2", Pin.INPUT),
        Pin(5, "S1", Pin.INPUT),
        Pin(6, "S0", Pin.INPUT),
        Pin(7, "~Cn", Pin.INPUT),
        Pin(8, "M", Pin.INPUT),
        Pin(9, "F0", Pin.OUTPUT),
        Pin(10, "F1", Pin.OUTPUT),
        Pin(11, "F2", Pin.OUTPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "F3", Pin.OUTPUT),
        Pin(14, "A=B", Pin.OUTPUT),
        Pin(15, "X", Pin.OUTPUT),
        Pin(16, "~Cn+4", Pin.OUTPUT),
        Pin(17, "Y", Pin.OUTPUT),
        Pin(18, "B3", Pin.INPUT),
        Pin(19, "A3", Pin.INPUT),
        Pin(20, "B2", Pin.INPUT),
        Pin(21, "A2", Pin.INPUT),
        Pin(22, "B1", Pin.INPUT),
        Pin(23, "A1", Pin.INPUT),
        Pin(24, "VCC", Pin.POWER),
    ]

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
            [[1] + bin2vec(s, 4) + bin2vec(v.a, 4) + bin2vec(v.b, 4), bin2vec(v.f, 4)]
            for v in data
        ]

        return Test(
            name=name,
            inputs=[8,  3, 4, 5, 6,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9],
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
                [0] + bin2vec(s, 4) + [v.c] + bin2vec(v.a, 4) + bin2vec(v.b, 4),
                bin2vec(v.f & 0b1111, 4) + [not v.f & 0b10000]
            ]
            for v in data
        ]
        return Test(
            name=name,
            inputs=[8,  3, 4, 5, 6,  7,  19, 21, 23, 2,  18, 20, 22, 1],
            outputs=[13, 11, 10, 9, 16],
            ttype=Test.COMB,
            loops=32,
            body=body
        )

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
        # TODO: A=B
        # TODO: G, P (X, Y)
    ]


# ------------------------------------------------------------------------
class Part74198(PartDIP24):
    name = "74198"
    desc = "8-bit shift registers"
    pins = [
        Pin(1, "S0", Pin.INPUT),
        Pin(2, "SR SER", Pin.INPUT),
        Pin(3, "A", Pin.INPUT),
        Pin(4, "QA", Pin.OUTPUT),
        Pin(5, "B", Pin.INPUT),
        Pin(6, "QB", Pin.OUTPUT),
        Pin(7, "C", Pin.INPUT),
        Pin(8, "QC", Pin.OUTPUT),
        Pin(9, "D", Pin.INPUT),
        Pin(10, "QD", Pin.OUTPUT),
        Pin(11, "CLK", Pin.INPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "~CLR", Pin.INPUT),
        Pin(14, "QE", Pin.OUTPUT),
        Pin(15, "E", Pin.INPUT),
        Pin(16, "QF", Pin.OUTPUT),
        Pin(17, "F", Pin.INPUT),
        Pin(18, "QG", Pin.OUTPUT),
        Pin(19, "G", Pin.INPUT),
        Pin(20, "QH", Pin.OUTPUT),
        Pin(21, "H", Pin.INPUT),
        Pin(22, "SL SER", Pin.INPUT),
        Pin(23, "S1", Pin.INPUT),
        Pin(24, "VCC", Pin.POWER),
    ]

    test_load = Test(
        name="Parallel load",
        inputs=[13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21],
        outputs=[4, 6, 8, 10, 14, 16, 18, 20],
        ttype=Test.SEQ,
        body=[
            [[1,  1, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  1, 1,  '+',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )
    test_clear = Test(
        name="Clear",
        inputs=[13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21],
        outputs=[4, 6, 8, 10, 14, 16, 18, 20],
        ttype=Test.SEQ,
        body=[
            # load 1s
            [[1,  1, 1,  '+',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            # clear
            [['-',  1, 1,  0,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
        ]
    )
    test_rshift = Test(
        name="Shift right",
        inputs=[13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21],
        outputs=[4, 6, 8, 10, 14, 16, 18, 20],
        ttype=Test.SEQ,
        body=[
            # clear
            [['0',  1, 1,  0,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # rshift
            [[1,  0, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0]],
            [[1,  0, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 0]],
            [[1,  0, 1,  '+',  0, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0]],
            [[1,  0, 1,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1]],
        ]
    )
    test_lshift = Test(
        name="Shift left",
        inputs=[13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21],
        outputs=[4, 6, 8, 10, 14, 16, 18, 20],
        ttype=Test.SEQ,
        body=[
            # clear
            [['-',  1, 1,  0,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # lshift
            [[1,  1, 0,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1]],
            [[1,  1, 0,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1]],
            [[1,  1, 0,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1]],
            [[1,  1, 0,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0]],
            [[1,  1, 0,  '+',  1, 0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1]],
            [[1,  1, 0,  '+',  0, 0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0]],
        ]
    )
    test_clk_inhibit = Test(
        name="Clock inhibit",
        inputs=[13,  23, 1,  11,  22, 2,  3, 5, 7, 9, 15, 17, 19, 21],
        outputs=[4, 6, 8, 10, 14, 16, 18, 20],
        ttype=Test.SEQ,
        body=[
            # clear
            [['-',  1, 1,  0,  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # clock inhibit
            [[1,  0, 0,  '+',  1, 1,  1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # load 1s
            [[1,  1, 1,  '+',  0, 0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            # clock inhibit
            [[1,  0, 0,  '+',  1, 1,  0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]],
        ]
    )

    tests = [test_load, test_clear, test_rshift, test_lshift, test_clk_inhibit]


# ------------------------------------------------------------------------
class Part4164(PartDIP16r):
    TEST_BIT_ALL_0 = 0
    TEST_BIT_ALL_1 = 1
    TEST_ROW_ALL_0 = 2
    TEST_ROW_ALL_1 = 3
    TEST_ROW_ALTERNATE_01 = 4
    TEST_ROW_ALTERNATE_10 = 5

    name = "4164"
    desc = "(also HM4864, ...) (REVERSE CHIP ORIENTATION!) 65536 x 1bit DRAM memory"
    pins = [
        Pin(1, "NC", Pin.NC),
        Pin(2, "Din", Pin.INPUT),
        Pin(3, "~WE", Pin.INPUT),
        Pin(4, "~RAS", Pin.INPUT),
        Pin(5, "A0", Pin.INPUT),
        Pin(6, "A2", Pin.INPUT),
        Pin(7, "A1", Pin.INPUT),
        Pin(8, "VCC", Pin.POWER),
        Pin(9, "A7", Pin.INPUT),
        Pin(10, "A5", Pin.INPUT),
        Pin(11, "A4", Pin.INPUT),
        Pin(12, "A3", Pin.INPUT),
        Pin(13, "A6", Pin.INPUT),
        Pin(14, "Dout", Pin.OUTPUT),
        Pin(15, "~CAS", Pin.INPUT),
        Pin(16, "GND", Pin.POWER),
    ]
    test_bit_all_0 = Test(
        name="Single bit: all 0s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_BIT_ALL_0,
        loops=1,
        body=[],
    )
    test_bit_all_1 = Test(
        name="Single bit: all 1s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_BIT_ALL_1,
        loops=1,
        body=[],
    )
    test_row_all_0 = Test(
        name="Page mode: all 0s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALL_0,
        loops=1,
        body=[],
    )
    test_row_all_1 = Test(
        name="Page mode: all 1s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALL_1,
        loops=1,
        body=[],
    )
    test_row_alternate_01 = Test(
        name="Page mode: alternating 0/1",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALTERNATE_01,
        loops=1,
        body=[],
    )
    test_row_alternate_10 = Test(
        name="Page mode: alternating 1/0",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALTERNATE_10,
        loops=1,
        body=[],
    )
 
    tests = [test_bit_all_0, test_bit_all_1, test_row_all_0, test_row_all_1, test_row_alternate_01, test_row_alternate_10]


# ------------------------------------------------------------------------
# build parts catalog
catalog = {}
for i in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(i[1]) and 'pins' in [i[0] for i in inspect.getmembers(i[1])]:
        catalog[i[1].name] = i[1]
