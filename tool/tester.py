import serial
import time
from binvec import BV


class Tester:
    CMD_HELLO = 1
    CMD_DUT_SETUP = 2
    CMD_TEST_SETUP = 3
    CMD_VECTORS_LOAD = 4
    CMD_RUN = 5
    CMD_DUT_CONNECT = 6
    CMD_DUT_DISCONNECT = 7

    RESP_HELLO = 129
    RESP_OK = 130
    RESP_PASS = 131
    RESP_FAIL = 132
    RESP_ERR = 133

    error_strings = {
        0: "Error code was not set",
        1: "Unknown command",
        2: "Unsupported package type",
        3: "Unsupported pin count",
        4: "Unknown pin function",
        5: "Unsupported test type",
        6: "Bad test parameters",
        7: "Wrong number of test vectors",
        8: "Missing DUT setup",
        9: "No test set",
        10: "No vectors loaded",
    }

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
        b = bytes(b)
        if self.serial_debug:
            data = [f"{x:08b} ({chr(x)})" for x in b]
            print(f"<- {data}")
        self.s.write(b)

    def recv(self):
        b = ord(self.s.read(1))
        if self.serial_debug:
            print(f"-> {b:>08b} {b}")
        return b

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def dut_setup(self):
        self.send([Tester.CMD_DUT_SETUP, self.part.package_type,  self.part.pincount])

        if self.debug:
            print("Pin roles:")

        for num, pin in sorted(self.part.pins.items()):
            if self.debug:
                print(f" {num:-2}: {pin.role_name}")
            self.send([pin.role])

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT setup failed")

    def get_pinvalue(self, pins, vals, pin):
        return 0 if pin not in pins else vals[pins.index(pin)]

    def test_setup(self, test):
        self.send([Tester.CMD_TEST_SETUP, test.type, test.subtype])

        data = [
            1 if i in test.inputs + test.outputs else 0
            for i in reversed(range(1, self.part.pincount+1))
        ]
        if self.debug:
            print(f"Pin used by the test: {data}")
        self.send(BV(data))

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if self.debug:
            print(f"Test vectors ({len(test.body)}):")
            for v in test.body:
                print(f" {v[0]} -> {v[1]}")

        assert len(test.body) <= Tester.MAX_LEN
        for v in test.body:
            assert len(test.inputs) == len(v[0])
            assert len(test.outputs) == len(v[1])

        self.send([Tester.CMD_VECTORS_LOAD])
        self.send(BV.int(len(test.body), 16))

        if self.debug:
            print("Binary vectors:")

        for v in test.body:
            data = [
                self.get_pinvalue(test.inputs + test.outputs, [*v[0], *v[1]], i)
                for i in reversed(range(1, self.part.pincount+1))
            ]
            if self.debug:
                print(f" {data}")
            self.send(BV(data))

        if self.recv() != Tester.RESP_OK:
            raise RuntimeError("Vectors load failed")

    def run(self, loop_pow):
        assert loop_pow < 16

        self.send([Tester.CMD_RUN, loop_pow])

        start = time.time()
        result = self.recv()
        elapsed = time.time() - start

        return result, elapsed

    def exec_test(self, test, loop_pow):
        self.dut_setup()
        self.test_setup(test)
        self.vectors_load(test)
        return self.run(loop_pow)
