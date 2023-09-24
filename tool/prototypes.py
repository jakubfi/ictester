import time
import math
import inspect
import logging
from enum import Enum
from struct import (pack, unpack)
from binvec import BV
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
TestType = Enum("TestType", names=[
        ("LOGIC", 1),
        ("DRAM", 2),
        ("UNIVIB", 3),
    ]
)
DRAMType = Enum("DRAMType", names=[
        ("DRAM_4164", 1),
        ("DRAM_41256", 2),
    ]
)
DRAMTestType = Enum("DRAMTestType", names=[
        ("SPEED_CHECK", 0),
        ("MARCH_C_MINUS_RMW", 1),
        ("MARCH_C_MINUS_RW", 2),
        ("MARCH_C_MINUS_PAGE", 3),
    ]
)
UnivibType = Enum("UnivibType", names=[
        ("UNI_74121", 0),
        ("UNI_74122", 1),
        ("UNI_74123_1", 2),
        ("UNI_74123_2", 3),
    ]
)
UnivibTestType = Enum("UnivibTestType", names=[
        ("NO_TRIGGER", 0),
        ("TRIGGER", 1),
        ("RETRIGGER", 2),
        ("CLEAR", 3),
        ("NO_CROSS_TRIGGER", 4),
        ("CLEAR_TRIGGER", 5),
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

        logger.info("DUT pin definitions, %s configuration(-s) available:", cfg_count)

        for cfgnum in range(0, cfg_count):
            logger.info("Configuration %s:", cfgnum)
            for num, pin in sorted(self.pins.items()):
                try:
                    pin_func = pin.zif_func[cfgnum]
                except IndexError:
                    pin_func = pin.zif_func[0]
                logger.info('%3s %6s %5s ZIF %s', num, pin.name, pin.role.name, pin_func.name)
                data.append(pin_func.value)

        return bytes(data)

    def setup(self, tr):
        logger.info("---- DUT SETUP ------------------------------------")
        data = bytes([CmdType.DUT_SETUP.value]) + bytes(self)
        tr.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("DUT setup failed")

    def connect(self, tr, cfgnum):
        logger.info("---- DUT CONNECT ----------------------------------")
        data = bytes([CmdType.DUT_CONNECT.value, cfgnum])
        r.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("DUT connect failed")

    def disconnect(self, tr):
        logger.info("---- DUT DISCONNECT -------------------------------")
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


# ------------------------------------------------------------------------
class TestVector():
    def __init__(self, vector, test):
        self.input = vector[0]
        self.output = vector[1] if vector[1] else []
        self.test = test

    def pin(self, pin):
        try:
            return [*self.input, *self.output][self.test.pins.index(pin)]
        except (IndexError, ValueError):
            return False

    def by_pins(self, pins):
        return [self.pin(i) for i in pins]

    def __str__(self):
        return f"{list(map(int, self.input))} -> {list(map(int, self.output))}"

    def __bytes__(self):
        pin_data = self.by_pins(sorted(self.test.part.pins))
        # If output is empty, that means DUT outputs shouldn't be checked
        # Protocol marks such case with "1" on VCC position
        if not self.output:
            for vcc in self.test.part.vcc:
                pin_data[vcc-1] = 1

        pin_data = list(reversed(pin_data))

        logger.info("%s%s", list(map(int, pin_data)), ' NC' if not self.output else '')

        return bytes(BV(pin_data))


# ------------------------------------------------------------------------
class Test:
    def __init__(self, ttype, name, loops=1024, cfgnum=0, read_delay_us=0):
        self.type = ttype
        self.name = name
        self.loops = loops
        self.cfgnum = cfgnum
        self.part = None
        self.elapsed = None
        self.read_delay_us = read_delay_us

    def attach_part(self, part):
        self.part = part

    def set_delay(self, read_delay_us):
        self.read_delay_us = read_delay_us

    def __bytes__(self):
        data = bytes([self.cfgnum, self.type.value])

        logger.info("Test type: %s", self.type.name)
        logger.info("Configuration used: %s", self.cfgnum)

        return data

    def setup(self, tr):
        logger.info("---- TEST SETUP -----------------------------------")
        data = bytes([CmdType.TEST_SETUP.value]) + bytes(self)
        tr.send(data)
        resp = Response(tr)
        if resp.response != RespType.OK:
            raise RuntimeError("Test setup failed")

    def run(self, tr, loops):
        logger.info("---- RUN ------------------------------------------")
        assert 1 <= loops <= 0xffff

        data = bytes([CmdType.RUN.value]) + pack("<H", loops)
        tr.send(data)

        start = time.time()
        resp = Response(tr)
        self.elapsed = time.time() - start

        return resp

# ------------------------------------------------------------------------
class TestDRAM(Test):
    def __init__(self, name, chip_type, chip_test_type, loops=1, cfgnum=0):
        super(TestDRAM, self).__init__(TestType.DRAM, name, loops, cfgnum)
        self.chip_test_type = chip_test_type
        self.chip_type = chip_type
        self.vectors = []

    @property
    def pins(self):
        return self.inputs + self.outputs

    def __bytes__(self):
        data = super().__bytes__()
        data += bytes([self.chip_type.value, self.chip_test_type.value])

        logger.info("DRAM chip: %s, test: %s", self.chip_type.name, self.chip_test_type.name)

        return data

    def run(self, tr, loops):
        resp = super().run(tr, loops)

        if resp.response == RespType.FAIL:
            self.failed_row, self.failed_column, self.failed_march_step = unpack("<HHB", resp.payload)

        return resp

# ------------------------------------------------------------------------
class TestUnivib(Test):
    def __init__(self, name, chip_type, chip_test_type, loops=1024, cfgnum=0):
        super(TestUnivib, self).__init__(TestType.UNIVIB, name, loops, cfgnum)
        self.chip_type = chip_type
        self.chip_test_type = chip_test_type
        self.vectors = []

    @property
    def pins(self):
        return self.inputs + self.outputs

    def __bytes__(self):
        data = super().__bytes__()
        data += bytes([self.chip_type.value, self.chip_test_type.value])

        logger.info("Univibrator: %s, test: %s", self.chip_type.name, self.chip_test_type.name)

        return data


# ------------------------------------------------------------------------
class TestLogic(Test):

    MAX_TEST_PARAMS = 2
    MAX_VECTORS = 1024

    def __init__(self, name, inputs, outputs, params=[], body=[], loops=1024, cfgnum=0, read_delay_us=0):
        super(TestLogic, self).__init__(TestType.LOGIC, name, loops, cfgnum, read_delay_us)
        self.params = params + [0] * (self.MAX_TEST_PARAMS - len(params))
        self.inputs = inputs
        self.outputs = outputs
        self._body = body
        self._vectors = None

    @property
    def pins(self):
        return self.inputs + self.outputs

    @property
    def _body_data(self):
        if callable(self._body):
            return self._body()
        else:
            return self._body

    @property
    def body(self):
        for v in self._body_data:
            i = v[0]
            o = v[1]
            if set(['+', '-']).intersection(i):
                yield [[0 if x == '+' else 1 if x == '-' else x for x in i], None]
                yield [[1 if x == '+' else 0 if x == '-' else x for x in i], None]
                yield [[0 if x == '+' else 1 if x == '-' else x for x in i], o]
            elif set(['/', '\\']).intersection(i):
                yield [[0 if x == '/' else 1 if x == '\\' else x for x in i], None]
                yield [[1 if x == '/' else 0 if x == '\\' else x for x in i], o]
            else:
                yield v

    @property
    def vectors(self):
        if not self._vectors:
            self._vectors = [TestVector(v, self) for v in self.body]
        return self._vectors

    def __bytes__(self):
        data = super().__bytes__()
        data += round(self.read_delay_us/0.2).to_bytes(2, 'little')

        pin_data = [
            1 if i in self.pins else 0
            for i in reversed(sorted(self.part.pins))
        ]
        logger.info("Additional read delay: %s μs", self.read_delay_us)
        logger.info("DUT inputs: %s", self.inputs)
        logger.info("DUT outputs: %s", self.outputs)

        data += bytes(BV(pin_data))

        return data

    def setup(self, tr):
        super().setup(tr)

        if logger.isEnabledFor(logging.INFO):
            logger.info("---- VECTORS LOAD ---------------------------------")
            logger.info("Test vectors (%s)", len(self.vectors))
            for v in self.vectors:
                logger.info(v)

        assert len(self.vectors) <= TestLogic.MAX_VECTORS

        # split vectors into chunks that fit in tester's buffer
        buf_size = 2048
        v_per_chunk = buf_size // math.ceil(self.part.pincount/8) - 2
        vector_chunks = [self.vectors[i:i+v_per_chunk] for i in range(0, len(self.vectors), v_per_chunk)]

        for vc in vector_chunks:
            logger.info("Binary vectors chunk sent (%s):", len(vc))
            data = bytes([CmdType.VECTORS_LOAD.value]) + pack("<H", len(vc))
            for v in vc:
                data += bytes(v)

            tr.send(data)

            resp = Response(tr)
            if resp.response != RespType.OK:
                raise RuntimeError("Vectors load failed")

    def run(self, tr, loops):
        resp = super().run(tr, loops)

        if resp.response == RespType.FAIL:
            self.failed_vector_num = unpack("<H", resp.payload[0:2])[0]
            self.failed_pin_vector = [*BV.int(resp.payload[2], 8).reversed()]
            self.failed_pin_vector.extend([*BV.int(resp.payload[3], 8).reversed()])
            if self.part.pincount > 16:
                self.failed_pin_vector.extend([*BV.int(resp.payload[4], 8).reversed()])

        return resp


