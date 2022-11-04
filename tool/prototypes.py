from functools import reduce

# ------------------------------------------------------------------------
class Pin:
    INPUT = 1
    OUTPUT = 2
    OC = 3
    VCC = 4
    GND = 5
    NC = 6

    def __init__(self, name, role):
        self.name = name
        self.role = role


# ------------------------------------------------------------------------
class Part:
    pincount = 0
    name = None
    package_name = None
    package_variant = None
    full_package_name = None
    missing = None
    unusual_power = False

    def __init__(self):
        assert self.name
        assert self.desc
        assert self.package_name

        for p in self.pin_cfg:
            if p in self.package_pins:
                raise RuntimeError(f"Duplicate pin {p} definition")

        pin_cfg_roles = [p.role for p in self.pin_cfg.values()]
        if Pin.VCC in pin_cfg_roles or Pin.GND in pin_cfg_roles:
            raise RuntimeError("VCC/GND pins should not be configured for a part. Package classes provide this.")

        self.pins = {}
        self.pins.update(self.package_pins)
        self.pins.update(self.pin_cfg)

        if len(self.pins) != self.pincount:
            raise RuntimeError(f"Number of pins for the part does not match package pincount: {self.pincount}")

        for p in self.pins:
            if p < 1 or p > self.pincount:
                raise RuntimeError(f"Wrong pin index for the package: {p}")

        pin_roles = [p.role for p in self.pins.values()]
        if Pin.VCC not in pin_roles or Pin.GND not in pin_roles:
            raise RuntimeError("VCC or GND pin missing")

        last_pin = self.pins[max(self.pins)]
        if last_pin.role != Pin.VCC:
            self.unusual_power = True
            vcc_pin = next(k for k, v in self.pins.items() if v.role == Pin.VCC)
            self.package_variant = f"VCC@pin{vcc_pin}"
            self.full_package_name = f"{self.package_name} {self.package_variant}"
        else:
            self.full_package_name = self.package_name

    def get_test(self, name):
        return next(t for t in self.tests if t.name == name)


# ------------------------------------------------------------------------
class PartDIP14(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        7: Pin("GND", Pin.GND),
        14: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PartDIP14_vcc5(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        10: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PartDIP14_vcc4(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        4: Pin("VCC", Pin.VCC),
        11: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PartDIP16(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        8: Pin("GND", Pin.GND),
        16: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PartDIP16_rotated(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        8: Pin("VCC", Pin.VCC),
        16: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PartDIP16_vcc5(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        12: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PartDIP24(Part):
    package_name = "DIP24"
    pincount = 24
    package_pins = {
        12: Pin("GND", Pin.GND),
        24: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class Test():
    COMB = 0
    SEQ = 1
    MEM = 2

    # ------------------------------------------------------------------------
    def __init__(self, name, ttype, inputs, outputs, body=[], tsubtype=0, loops=1024):
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

