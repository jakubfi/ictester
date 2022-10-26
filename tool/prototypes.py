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
class PartDIP14x(Part):
    package_name = "DIP14x"
    pincount = 14


# ------------------------------------------------------------------------
class PartDIP14x2(Part):
    package_name = "DIP14x2"
    pincount = 14


# ------------------------------------------------------------------------
class PartDIP16(Part):
    package_name = "DIP16"
    pincount = 16


# ------------------------------------------------------------------------
class PartDIP16r(Part):
    package_name = "DIP16r"
    pincount = 16


# ------------------------------------------------------------------------
class PartDIP16x(Part):
    package_name = "DIP16x"
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
