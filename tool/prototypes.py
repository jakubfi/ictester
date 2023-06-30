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
    VCC = 4     # +5V power
    GND = 5     # ground
    NC = 6      # unused pin

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
    missing_tests = None
    unusual_power = False

    def __init__(self):
        assert self.name
        assert self.desc
        assert self.package_name
        assert self.tests

        for p in self.pin_cfg:
            if p in self.package_pins:
                raise RuntimeError(f"Duplicate pin {p} definition for {self.name}")

        pin_cfg_roles = [p.role for p in self.pin_cfg.values()]
        if Pin.VCC in pin_cfg_roles or Pin.GND in pin_cfg_roles:
            raise RuntimeError(f"VCC/GND pins should not be configured for {self.name}. Package classes provide this.")

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
class PackageDIP14(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        7: Pin("GND", Pin.GND),
        14: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc5(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        10: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc4(Part):
    package_name = "DIP14"
    pincount = 14
    package_pins = {
        4: Pin("VCC", Pin.VCC),
        11: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        8: Pin("GND", Pin.GND),
        16: Pin("VCC", Pin.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP16_rotated(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        8: Pin("VCC", Pin.VCC),
        16: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16_vcc5(Part):
    package_name = "DIP16"
    pincount = 16
    package_pins = {
        5: Pin("VCC", Pin.VCC),
        12: Pin("GND", Pin.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP24(Part):
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
        self.name = name
        self.type = ttype
        self.subtype = tsubtype
        self.loops = loops
        self._body = body
        self.inputs = inputs
        self.outputs = outputs

    @property
    def body(self):
        if callable(self._body):
            return self._body()
        else:
            return self._body

