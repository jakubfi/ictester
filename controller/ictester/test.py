import time
import math
import logging
from enum import Enum
from struct import (pack, unpack)
from ictester.binvec import BV
from ictester.command import CmdType
from ictester.response import (Response, RespType)

logger = logging.getLogger('ictester')

# ------------------------------------------------------------------------
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

        logger.log(19, "%s%s", list(map(int, pin_data)), ' NC' if not self.output else '')

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

        logger.log(20, "Test type: %s", self.type.name)
        logger.log(20, "Configuration used: %s", self.cfgnum)

        return data

    def setup(self, tr):
        logger.log(20, "---- TEST SETUP -----------------------------------")
        data = bytes([CmdType.TEST_SETUP.value]) + bytes(self)
        tr.send(data)
        resp = Response(tr)

    def run(self, tr, loops):
        logger.log(20, "---- RUN ------------------------------------------")
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

        logger.log(20, "DRAM chip: %s, test: %s", self.chip_type.name, self.chip_test_type.name)

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

        logger.log(20, "Univibrator: %s, test: %s", self.chip_type.name, self.chip_test_type.name)

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
        logger.log(20, "Additional read delay: %s μs", self.read_delay_us)
        logger.log(20, "DUT inputs: %s", self.inputs)
        logger.log(20, "DUT outputs: %s", self.outputs)

        data += bytes(BV(pin_data))

        return data

    def setup(self, tr):
        super().setup(tr)

        if logger.isEnabledFor(20):
            logger.log(20, "---- VECTORS LOAD ---------------------------------")
            logger.log(20, "Test vectors (%s)", len(self.vectors))
            for v in self.vectors:
                logger.log(19, v)

        assert len(self.vectors) <= TestLogic.MAX_VECTORS

        # split vectors into chunks that fit in tester's buffer
        buf_size = 2048
        v_per_chunk = buf_size // math.ceil(self.part.pincount/8) - 2
        vector_chunks = [self.vectors[i:i+v_per_chunk] for i in range(0, len(self.vectors), v_per_chunk)]

        for vc in vector_chunks:
            logger.log(20, "Binary vectors chunk sent (%s)", len(vc))
            data = bytes([CmdType.VECTORS_LOAD.value]) + pack("<H", len(vc))
            for v in vc:
                data += bytes(v)

            tr.send(data)

            resp = Response(tr)

    def run(self, tr, loops):
        resp = super().run(tr, loops)

        if resp.response == RespType.FAIL:
            self.failed_loop = unpack("<H", resp.payload[0:2])[0]
            self.failed_vector_num = unpack("<H", resp.payload[2:4])[0]
            self.failed_pin_vector = [*BV.int(resp.payload[4], 8).reversed()]
            self.failed_pin_vector.extend([*BV.int(resp.payload[5], 8).reversed()])
            if self.part.pincount > 16:
                self.failed_pin_vector.extend([*BV.int(resp.payload[6], 8).reversed()])

        return resp


