import sys
import inspect
from prototypes import (Test, Pin, PartDIP14, PartDIP16)


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
    vector_in = [1, 2, 4, 5, 10, 9, 13, 12]
    vector_out = [3, 6, 8, 11]
    test = [
            [[0, 0,  0, 0,  0, 0,  0, 0], [1, 1, 1, 1]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [1, 1, 1, 1]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [1, 1, 1, 1]],
            [[1, 1,  1, 1,  1, 1,  1, 1], [0, 0, 0, 0]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
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
    vector_in = [2, 3, 5, 6, 8, 9, 11, 12]
    vector_out = [1, 4, 10, 13]
    test = [
            [[0, 0,  0, 0,  0, 0,  0, 0], [1, 1, 1, 1]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [0, 0, 0, 0]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [0, 0, 0, 0]],
            [[1, 1,  1, 1,  1, 1,  1, 1], [0, 0, 0, 0]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
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
    vector_in = [1, 3, 5, 9, 11, 13]
    vector_out = [2, 4, 6, 8, 10, 12]
    test = [
            [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]],
            [[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
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
    vector_in = [1, 2, 4, 5, 10, 9, 13, 12]
    vector_out = [3, 6, 8, 11]
    test = [
            [[0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [0, 0, 0, 0]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [0, 0, 0, 0]],
            [[1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
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
    vector_in = [1, 2, 13, 3, 4, 5, 9, 10, 11]
    vector_out = [12, 6, 8]
    test = [
            [[0, 0, 0,  0, 0, 0,  0, 0, 0], [1, 1, 1]],
            [[0, 0, 1,  0, 0, 1,  0, 0, 1], [1, 1, 1]],
            [[0, 1, 0,  0, 1, 0,  0, 1, 0], [1, 1, 1]],
            [[0, 1, 1,  0, 1, 1,  0, 1, 1], [1, 1, 1]],
            [[1, 0, 0,  1, 0, 0,  1, 0, 0], [1, 1, 1]],
            [[1, 0, 1,  1, 0, 1,  1, 0, 1], [1, 1, 1]],
            [[1, 1, 0,  1, 1, 0,  1, 1, 0], [1, 1, 1]],
            [[1, 1, 1,  1, 1, 1,  1, 1, 1], [0, 0, 0]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
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
    vector_in = [1, 2, 4, 5, 13, 12, 10, 9]
    vector_out = [6, 8]
    test = [
            [[0, 0, 0, 0,  0, 0, 0, 0], [1, 1]],
            [[0, 0, 0, 1,  0, 0, 0, 1], [1, 1]],
            [[0, 0, 1, 0,  0, 0, 1, 0], [1, 1]],
            [[0, 0, 1, 1,  0, 0, 1, 1], [1, 1]],
            [[0, 1, 0, 0,  0, 1, 0, 0], [1, 1]],
            [[0, 1, 0, 1,  0, 1, 0, 1], [1, 1]],
            [[0, 1, 1, 0,  0, 1, 1, 0], [1, 1]],
            [[0, 1, 1, 1,  0, 1, 1, 1], [1, 1]],
            [[1, 0, 0, 0,  1, 0, 0, 0], [1, 1]],
            [[1, 0, 0, 1,  1, 0, 0, 1], [1, 1]],
            [[1, 0, 1, 0,  1, 0, 1, 0], [1, 1]],
            [[1, 0, 1, 1,  1, 0, 1, 1], [1, 1]],
            [[1, 1, 0, 0,  1, 1, 0, 0], [1, 1]],
            [[1, 1, 0, 1,  1, 1, 0, 1], [1, 1]],
            [[1, 1, 1, 0,  1, 1, 1, 0], [1, 1]],
            [[1, 1, 1, 1,  1, 1, 1, 1], [0, 0]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
    ]


# ------------------------------------------------------------------------
class Part7420(Part7413):
    name = "7420"
    desc = "Dual 4-input positive-NAND gates"


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
    vector_in = [1, 2, 4, 5, 10, 9, 13, 12]
    vector_out = [3, 6, 8, 11]
    test = [
            [[0, 0,  0, 0,  0, 0,  0, 0], [0, 0, 0, 0]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [1, 1, 1, 1]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [1, 1, 1, 1]],
            [[1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
    ]
    tests = [
        Test("Complete logic", Test.COMB, test),
    ]


# ------------------------------------------------------------------------
class Part7437(Part7400):
    name = "7437"
    desc = "Quad 2-input positive-NAND buffers"


# ------------------------------------------------------------------------
class Part7474(PartDIP14):
    name = "7474"
    desc = "Dual D-type positive-edge-triggered flip-flops with preset and clear"
    pins = [
        Pin(1, "1~CLR", Pin.INPUT),
        Pin(2, "1D", Pin.INPUT),
        Pin(3, "1CLK", Pin.INPUT),
        Pin(4, "1~PRE", Pin.INPUT),
        Pin(5, "1Q", Pin.OUTPUT),
        Pin(6, "1~Q", Pin.OUTPUT),
        Pin(7, "GND", Pin.POWER),
        Pin(8, "2~Q", Pin.OUTPUT),
        Pin(9, "2Q", Pin.OUTPUT),
        Pin(10, "2~PRE", Pin.INPUT),
        Pin(11, "2CLK", Pin.INPUT),
        Pin(12, "2D", Pin.INPUT),
        Pin(13, "2~CLR", Pin.INPUT),
        Pin(14, "VCC", Pin.POWER),
    ]
    vector_in = [1, 4, 2, 3, 13, 10, 12, 11]
    vector_out = [5, 6, 9, 8]
    sync_test = [
        [[1, 1, 0, 0,  1, 1, 0, 0], [0, 0,  0, 0]],
        [[1, 1, 0, 1,  1, 1, 0, 1], [0, 1,  0, 1]],
        [[1, 1, 1, 0,  1, 1, 1, 0], [0, 0,  0, 0]],
        [[1, 1, 1, 1,  1, 1, 1, 1], [1, 0,  1, 0]],
    ]
    async_test = [
        [[0, 1, 0, 0,  0, 1, 0, 0], [0, 1,  0, 1]],
        [[1, 0, 0, 0,  1, 0, 0, 0], [1, 0,  1, 0]],
    ]
    tests = [
        Test("Synchronous operation", Test.SEQ, sync_test),
        Test("Asynchronous operation", Test.SEQ, async_test),
    ]


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
    vector_in = [6, 8, 9, 1, 2, 3, 4, 5]
    vector_out = [13, 12, 11, 10]
    test_parallel = [
        [[1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
    ]
    test_rshift = [
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 0, 0]],
        [[0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0]],
        [[0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0]],
        [[0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 1, 0]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 1]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1]],
        [[0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0]],
        [[0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 1, 0]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 1]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1]],
        [[0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
    ]
    tests = [
        Test("Parallel load", Test.SEQ, test_parallel),
        Test("Right Shift", Test.SEQ, test_rshift),
    ]


# ------------------------------------------------------------------------
class Part74153(PartDIP16):
    name = "74153"
    desc = "Dual 4-line to 1-line data selectors/multiplexers"
    pins = [
        Pin(1, "1~G", Pin.INPUT),
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
        Pin(15, "2~G", Pin.INPUT),
        Pin(16, "VCC", Pin.POWER),
    ]
    vector_in = [2, 14, 1, 3, 4, 5, 6, 15, 13, 12, 11, 10]
    vector_out = [7, 9]
    test = [
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
    tests = [
        Test("Complete logic", Test.COMB, test),
    ]


# ------------------------------------------------------------------------
class Part74181(PartDIP24):
    name = "74181"
    desc = "Arithmetic logic units/function generators"
    pins = [
        Pin(1, "B~0", Pin.INPUT),
        Pin(2, "A~0", Pin.INPUT),
        Pin(3, "S3", Pin.INPUT),
        Pin(4, "S2", Pin.INPUT),
        Pin(5, "S1", Pin.INPUT),
        Pin(6, "S0", Pin.INPUT),
        Pin(7, "Cn", Pin.INPUT),
        Pin(8, "M", Pin.INPUT),
        Pin(9, "F~0", Pin.OUTPUT),
        Pin(10, "F~1", Pin.OUTPUT),
        Pin(11, "F~2", Pin.OUTPUT),
        Pin(12, "GND", Pin.POWER),
        Pin(13, "F~3", Pin.OUTPUT),
        Pin(14, "A=B", Pin.OUTPUT),
        Pin(15, "~P", Pin.OUTPUT),
        Pin(16, "Cn+4", Pin.OUTPUT),
        Pin(17, "~G", Pin.OUTPUT),
        Pin(18, "B~3", Pin.INPUT),
        Pin(19, "A~3", Pin.INPUT),
        Pin(20, "B~2", Pin.INPUT),
        Pin(21, "A~2", Pin.INPUT),
        Pin(22, "B~1", Pin.INPUT),
        Pin(23, "A~1", Pin.INPUT),
        Pin(24, "VCC", Pin.POWER),
    ]
    vector_in = [8, 3, 4, 5, 6,  7,  19, 21, 23, 2,  18, 20, 22, 1]
    vector_out = [13, 11, 10, 9,  16, 14,  17, 15]
    test_add = [
        # M  S3 S2 S1 S0  C   A            B             F            C  A=B G  P
        [[0, 1, 1, 1, 1,  0,  1, 1, 1, 1,  1, 1, 1, 1], [1, 1, 1, 1,  0, 0,  0, 0]],
    ]
    tests = [
        Test("Addition", Test.COMB, test_add),
    ]


# build parts catalog
catalog = {}
for i in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(i[1]) and 'vector_in' in [i[0] for i in inspect.getmembers(i[1])]:
        catalog[i[1].name] = i[1]
