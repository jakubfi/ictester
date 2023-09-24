import inspect
import logging
from enum import Enum
from command import CmdType
from response import (Response, RespType)

logger = logging.getLogger('ictester')

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
PinType = Enum("PinType", ["IN", "OUT", "BIDI", "OC", "ST3", "OE", "C", "RC", "VCC", "GND", "NC"])
ZIFFunc = Enum("ZIFFunc", names=[
        ("OUT", 1),
        ("IN_HIZ", 2),
        ("IN_PU_STRONG", 3),
        ("IN_PU_WEAK", 4),
        ("OUT_SINK", 5),
        ("C", 6),
        ("OUT_SOURCE", 7),
        ("VCC", 128),
        ("GND", 129),
    ]
)
Package = Enum("Package",
    names=[
        ("DIP", 1),
    ]
)

# ------------------------------------------------------------------------
class Pin:

    _pin_zif_allowed_funcs = {
        PinType.IN: [ZIFFunc.OUT],
        PinType.OUT: [ZIFFunc.IN_PU_WEAK, ZIFFunc.IN_PU_STRONG, ZIFFunc.IN_HIZ],
        PinType.BIDI: [ZIFFunc.OUT, ZIFFunc.IN_PU_WEAK, ZIFFunc.IN_PU_STRONG, ZIFFunc.IN_HIZ],
        PinType.OC: [ZIFFunc.IN_PU_STRONG, ZIFFunc.IN_PU_WEAK, ZIFFunc.IN_HIZ],
        PinType.ST3: [ZIFFunc.IN_PU_WEAK, ZIFFunc.IN_HIZ, ZIFFunc.IN_PU_STRONG],
        PinType.OE: [ZIFFunc.OUT_SINK],
        PinType.C: [ZIFFunc.C],
        PinType.RC: [ZIFFunc.IN_PU_STRONG],
        PinType.VCC: [ZIFFunc.VCC],
        PinType.GND: [ZIFFunc.GND],
        PinType.NC: [ZIFFunc.IN_HIZ],
    }

    _pin_zif_default_funcs = {
        PinType.IN: [ZIFFunc.OUT],
        PinType.OUT: [ZIFFunc.IN_PU_WEAK],
        PinType.BIDI: None,
        PinType.OC: [ZIFFunc.IN_PU_STRONG],
        PinType.ST3: [ZIFFunc.IN_PU_WEAK],
        PinType.OE: [ZIFFunc.OUT_SINK],
        PinType.C: [ZIFFunc.C],
        PinType.RC: [ZIFFunc.IN_PU_STRONG],
        PinType.VCC: [ZIFFunc.VCC],
        PinType.GND: [ZIFFunc.GND],
        PinType.NC: [ZIFFunc.IN_HIZ],
    }

    def __init__(self, name, role, zif_func=None):
        assert role in self._pin_zif_allowed_funcs
        self.name = name
        self.role = role

        if zif_func:
            self.zif_func = zif_func
        else:
            self.zif_func = self._pin_zif_default_funcs[role]

        if not self.zif_func:
                raise ValueError(f"Pin {self.name} which is of type {self.role.name} requires zif_func to be defined")
        else:
            for f in self.zif_func:
                if f not in self._pin_zif_allowed_funcs[role]:
                    raise ValueError(f"ZIF function: {f.name} cannot be assigned to pin type: {self.role.name}")


# ------------------------------------------------------------------------
class Part:
    pincount = 0
    package_type = None
    package_pins = {}
    name = None
    tests = None
    missing_tests = None

    def __init__(self):
        self.pins = {}
        self.pins.update(self.package_pins)
        self.pins.update(self.pin_cfg)

        for t in self.tests:
            t.attach_part(self)

    @property
    def package_name(self):
        return f"{self.package_type.name}{self.pincount}"

    @property
    def vcc(self):
        return list(k for k, v in self.pins.items() if v.role == PinType.VCC)

    @property
    def gnd(self):
        return list(k for k, v in self.pins.items() if v.role == PinType.GND)

    def __bytes__(self):
        data = []
        cfg_count = 0
        for pin in self.pins.values():
            if len(pin.zif_func) > cfg_count:
                cfg_count = len(pin.zif_func)
        assert 5 > cfg_count > 0
        data.extend([self.package_type.value, self.pincount, cfg_count])

        logger.log(20, "DUT pin definitions, %s configuration(-s) available:", cfg_count)

        for cfgnum in range(0, cfg_count):
            logger.log(20, "Configuration %s:", cfgnum)
            for num, pin in sorted(self.pins.items()):
                try:
                    pin_func = pin.zif_func[cfgnum]
                except IndexError:
                    pin_func = pin.zif_func[0]
                logger.log(20, '%3s %6s %5s ZIF %s', num, pin.name, pin.role.name, pin_func.name)
                data.append(pin_func.value)

        return bytes(data)

    def setup(self, tr):
        logger.log(20, "---- DUT SETUP ------------------------------------")
        data = bytes([CmdType.DUT_SETUP.value]) + bytes(self)
        tr.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("DUT setup failed")

    def connect(self, tr, cfgnum):
        logger.log(20, "---- DUT CONNECT ----------------------------------")
        data = bytes([CmdType.DUT_CONNECT.value, cfgnum])
        r.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("DUT connect failed")

    def disconnect(self, tr):
        logger.log(20, "---- DUT DISCONNECT -------------------------------")
        data = bytes([CmdType.DUT_DISCONNECT.value])
        tr.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("DUT disconnect failed")


# ------------------------------------------------------------------------
class PackageDIP14(Part):
    pincount = 14
    package_type = Package.DIP
    package_pins = {
        7: Pin("GND", PinType.GND),
        14: Pin("VCC", PinType.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc5(Part):
    pincount = 14
    package_type = Package.DIP
    package_pins = {
        5: Pin("VCC", PinType.VCC),
        10: Pin("GND", PinType.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP14_vcc4(Part):
    pincount = 14
    package_type = Package.DIP
    package_pins = {
        4: Pin("VCC", PinType.VCC),
        11: Pin("GND", PinType.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16(Part):
    pincount = 16
    package_type = Package.DIP
    package_pins = {
        8: Pin("GND", PinType.GND),
        16: Pin("VCC", PinType.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP16_rotated(Part):
    pincount = 16
    package_type = Package.DIP
    package_pins = {
        8: Pin("VCC", PinType.VCC),
        16: Pin("GND", PinType.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16_vcc5(Part):
    pincount = 16
    package_type = Package.DIP
    package_pins = {
        5: Pin("VCC", PinType.VCC),
        12: Pin("GND", PinType.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP16_vcc5_gnd13(Part):
    pincount = 16
    package_type = Package.DIP
    package_pins = {
        5: Pin("VCC", PinType.VCC),
        13: Pin("GND", PinType.GND),
    }


# ------------------------------------------------------------------------
class PackageDIP20(Part):
    pincount = 20
    package_type = Package.DIP
    package_pins = {
        10: Pin("GND", PinType.GND),
        20: Pin("VCC", PinType.VCC),
    }


# ------------------------------------------------------------------------
class PackageDIP24(Part):
    pincount = 24
    package_type = Package.DIP
    package_pins = {
        12: Pin("GND", PinType.GND),
        24: Pin("VCC", PinType.VCC),
    }

