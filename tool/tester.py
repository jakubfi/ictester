import serial
import time
import math
from binvec import BV


class Tester:
    CMD_HELLO = 1
    CMD_DUT_SETUP = 2
    CMD_TEST_SETUP = 3
    CMD_VECTORS_LOAD = 4
    CMD_RUN = 5

    RESP_HELLO = 129
    RESP_OK = 130
    RESP_PASS = 131
    RESP_FAIL = 132
    RESP_ERR = 133

    MAX_LEN = 1024

    def __init__(self, part, port, speed, debug=False, serial_debug=False):
        self.part = part

        if len(self.tests_available()) != len(set(self.tests_available())):
            raise RuntimeError(f"Test names for part {part.name} are not unique")

        self.port = port
        self.speed = speed
        self.debug = debug
        self.serial_debug = serial_debug
        self._s = None

    @property
    def s(self):
        if not self._s:
            self._s = serial.Serial(
                self.port,
                baudrate=self.speed,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=None,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
        return self._s

    def send(self, b):
        if self.serial_debug:
            print(f"<- {b:>08b} {b}")
        data = bytes([b])
        self.s.write(data)

    def send_16le(self, w):
        self.send(w & 0xff)
        self.send((w >> 8) & 0xff)

    def send_vector_as_bytes(self, v):
        data = int(BV(v))
        if self.debug:
            print(f" {data:0{len(v)}b}")
        for shift in [0, 8, 16][0:math.ceil(len(v)/8)]:
            self.send((data >> shift) & 0xff)

    def recv(self):
        b = ord(self.s.read(1))
        if self.serial_debug:
            print(f"-> {b:>08b} {b}")
        return b

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def dut_setup(self):
        if self.debug:
            print("Pin roles:")

        self.send(Tester.CMD_DUT_SETUP)
        self.send(self.part.package_type)
        self.send(self.part.pincount)

        for num, pin in sorted(self.part.pins.items()):
            if self.debug:
                print(f" {num:-2}: {pin.role_name}")
            self.send(pin.role)

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT setup failed")

    def get_pinvalue(self, pins, vals, pin):
        return 0 if pin not in pins else vals[pins.index(pin)]

    def sequentialize(self, v):
        i = v[0]
        o = v[1]
        return [
            [[x if x in [0, 1] else 0 if x == '+' else 1 for x in i], o],
            [[x if x in [0, 1] else 1 if x == '+' else 0 for x in i], o],
        ]

    def test_setup(self, test):
        self.send(Tester.CMD_TEST_SETUP)
        self.send(test.type)
        self.send(test.subtype)

        if self.debug:
            print("Pin used by the test:")

        data = [
            1 if i in test.inputs + test.outputs else 0
            for i in reversed(range(1, self.part.pincount+1))
        ]
        self.send_vector_as_bytes(data)

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):

        if test.type == test.COMB:
            body = test.body
        else:
            body = []
            for t in test.body:
                body.extend(self.sequentialize(t))

        if self.debug:
            print(f"Test vectors ({len(body)}):")
            for v in body:
                print(f" {v[0]} -> {v[1]}")

        assert len(body) <= Tester.MAX_LEN
        for v in body:
            assert len(test.inputs) == len(v[0])
            assert len(test.outputs) == len(v[1])

        self.send(Tester.CMD_VECTORS_LOAD)
        self.send_16le(len(body))

        if self.debug:
            print("Binary vectors:")

        for v in body:
            data = [
                self.get_pinvalue(test.inputs + test.outputs, [*v[0], *v[1]], i)
                for i in reversed(range(1, self.part.pincount+1))
            ]
            self.send_vector_as_bytes(data)

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("Vectors load failed")

    def run(self, loop_pow):
        assert loop_pow < 16

        self.send(Tester.CMD_RUN)
        self.send(loop_pow)

        start = time.time()
        result = self.recv()
        elapsed = time.time() - start

        return result, elapsed

    def exec_test(self, test, loop_pow):
        self.dut_setup()
        self.test_setup(test)
        self.vectors_load(test)
        return self.run(loop_pow)
