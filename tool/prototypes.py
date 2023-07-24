import inspect

# ------------------------------------------------------------------------
def partimport(part_name):
    '''
    Since module names cannot start with a number... Nasty hack time!
    '''
    part_module = __import__(f'parts.{part_name}', fromlist=[f'Part{part_name}'])
    class_list = inspect.getmembers(part_module, lambda x: inspect.isclass(x) and x.__name__ == f'Part{part_name}')
    assert len(class_list) == 1
    return class_list[0][1]

# ------------------------------------------------------------------------
class Pin:
    IN = 1      # regular TTL input
    OUT = 2     # regular TTL output
    OC = 3      # open-collector output
    VCC = 128   # +5V power
    GND = 129   # ground
    NC = 255    # unused pin

    _role_names = {
        IN: "IN",
        OUT: "OUT",
        OC: "OC",
        VCC: "VCC",
        GND: "GND",
        NC: "NC",
    }

    def __init__(self, name, role):
        assert role in self._role_names
        self.name = name
        self.role = role

    @property
    def role_name(self):
        return self._role_names[self.role]


# ------------------------------------------------------------------------
class Part:

    DIP = 1

    _type_names = {
        DIP: "DIP",
    }

    pincount = 0
    name = None
    tests = None
    missing_tests = None

    def __init__(self):
        self.pins = {}
        self.pins.update(self.package_pins)
        self.pins.update(self.pin_cfg)

    def get_test(self, name):
        return next(t for t in self.tests if t.name == name)

    @property
    def package_name(self):
        return f"{self._type_names[self.package_type]}{self.pincount}"

    @property
    def unusual_power(self):
        return self.pins[max(self.pins)].role != Pin.VCC

    @property
    def package_variant(self):
        vcc_pin = next(k for k, v in self.pins.items() if v.role == Pin.VCC)
        return f"VCC@pin{vcc_pin}"

    @property
    def full_package_name(self):
        return f"{self.package_name} {self.package_variant}" if self.unusual_power else self.package_name


# ------------------------------------------------------------------------
class PackageDIP14(Part):
    pincount = 14
    package_type = Part.DIP
    package_pins = {
        7: Pin("GND", Pin.GND),
        14: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc5(Part):
    pincount = 14
    package_type = Part.DIP
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        10: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc4(Part):
    pincount = 14
    package_type = Part.DIP
    package_pins = {
        4: Pin("VCC", Pin.VCC),
        11: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16(Part):
    pincount = 16
    package_type = Part.DIP
    package_pins = {
        8: Pin("GND", Pin.GND),
        16: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP16_rotated(Part):
    pincount = 16
    package_type = Part.DIP
    package_pins = {
        8: Pin("VCC", Pin.VCC),
        16: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16_vcc5(Part):
    pincount = 16
    package_type = Part.DIP
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        12: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP24(Part):
    pincount = 24
    package_type = Part.DIP
    package_pins = {
        12: Pin("GND", Pin.GND),
        24: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class TestVector():
    def __init__(self, vector, test):
        self.input = vector[0]
        self.output = vector[1]
        self.test = test

    def pin(self, pin):
        if pin not in self.test.pins:
            return 0
        else:
            return [*self.input, *self.output][self.test.pins.index(pin)]

    def by_pins(self, pins):
        return [self.pin(i) for i in pins]

    def __str__(self):
        return f"{self.input} -> {self.output}"

# ------------------------------------------------------------------------
class Test():
    COMB = 0
    SEQ = 1
    MEM = 2

    TEST_LOGIC_74 = 1
    TEST_DRAM_41 = 2

    MAX_TEST_PARAMS = 4

    def __init__(self, name, ttype, inputs, outputs, params=[], body=[], loops=1024):
        self.name = name
        self.type = ttype
        self.params = params + [0] * (self.MAX_TEST_PARAMS - len(params))
        self.loops = loops
        self._body_source = body
        self._body_generated = None
        self.inputs = inputs
        self.outputs = outputs

    @property
    def _body_data(self):
        if callable(self._body_source):
            return self._body_source()
        else:
            return self._body_source

    def sequentialize(self, v):
        i = v[0]
        o = v[1]
        return [
            [[x if x in [0, 1] else 0 if x == '+' else 1 for x in i], o],
            [[x if x in [0, 1] else 1 if x == '+' else 0 for x in i], o],
        ]

    @property
    def body(self):
        if not self._body_generated:
            if self.type == Test.COMB:
                self._body_generated = self._body_data
            else:
                self._body_generated = []
                for t in self._body_data:
                    self._body_generated.extend(self.sequentialize(t))

        return self._body_generated

    @property
    def pins(self):
        return self.inputs + self.outputs

    @property
    def vectors(self):
        for v in self.body:
            yield TestVector(v, self)
