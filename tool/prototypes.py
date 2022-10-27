from functools import reduce

# ------------------------------------------------------------------------
class Pin:
    INPUT = 1
    OUTPUT = 2
    OC = 3
    POWER = 4
    NC = 5

    def __init__(self, pin, name, role):
        self.pin = pin
        self.name = name
        self.role = role


# ------------------------------------------------------------------------
class Part:
    pincount = 0
    name = None
    package_name = None
    missing = ""

    def __init__(self):
        assert self.name
        assert self.desc
        assert self.package_name
        assert len(self.pins) == self.pincount
        for i in range(0, self.pincount):
            assert self.pins[i].pin-1 == i

    def get_test(self, name):
        return next(t for t in self.tests if t.name == name)


# ------------------------------------------------------------------------
class PartDIP14(Part):
    package_name = "DIP14"
    pincount = 14


# ------------------------------------------------------------------------
class PartDIP14_vcc5(Part):
    package_name = "DIP14, VCC@pin5"
    pincount = 14


# ------------------------------------------------------------------------
class PartDIP14_vcc4(Part):
    package_name = "DIP14, VCC@pin4"
    pincount = 14


# ------------------------------------------------------------------------
class PartDIP16(Part):
    package_name = "DIP16"
    pincount = 16


# ------------------------------------------------------------------------
class PartDIP16_rotated(Part):
    package_name = "DIP16 rotated, VCC@pin8"
    pincount = 16


# ------------------------------------------------------------------------
class PartDIP16_vcc5(Part):
    package_name = "DIP16, VCC@pin5"
    pincount = 16


# ------------------------------------------------------------------------
class PartDIP24(Part):
    package_name = "DIP24"
    pincount = 24


# ------------------------------------------------------------------------
class Test():
    COMB = 0
    SEQ = 1
    MEM = 2

    # ------------------------------------------------------------------------
    def __init__(self, name, ttype, inputs, outputs, body, tsubtype=0, loops=1024):
        assert name
        assert ttype in [Test.COMB, Test.SEQ, Test.MEM]
        assert inputs
        assert outputs
        if ttype in [Test.COMB, Test.SEQ]:
            assert body
            for v in body:
                assert len(inputs) == len(v[0])
                assert len(outputs) == len(v[1])
        self.name = name
        self.type = ttype
        self.subtype = tsubtype
        self.loops = loops
        self.body = body
        self.inputs = inputs
        self.outputs = outputs

    # ------------------------------------------------------------------------
    # Translate integer value into a binary vector
    # bin2vec(9, 7) -> [0, 0, 0, 1, 0, 0, 1]
    @staticmethod
    def bin2vec(val, bitlen):
        return [
            (val >> (bitlen-pos-1)) & 1
            for pos in range(0, bitlen)
        ]
    
    # ------------------------------------------------------------------------
    # Get all bit combinations for given bit length
    # binary_combinator(2) -> [[0, 0], [0, 1], [1, 0], [1, 1]]
    @staticmethod
    def binary_combinator(bitlen):
        return [
            Test.bin2vec(v, bitlen)
            for v in range(0, 2**bitlen)
        ]
    
    # ------------------------------------------------------------------------
    # Prepare test vectors for unit_cnt separate units with input_cnt inputs doing fun
    # Units are tested inm parallel
    # Four 3-input OR gates: binary_fun_gen(4, 3, lambda a, b: a|b)
    @staticmethod
    def binary_fun_gen(unit_cnt, input_cnt, fun, inverted=False):
        return [
            [unit_cnt*v, unit_cnt*[reduce(fun, v) if not inverted else not reduce(fun, v)]]
            for v in Test.binary_combinator(input_cnt)
        ]

