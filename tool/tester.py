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

    def __init__(self, part, transport, debug=False):
        self.part = part
        self.tr = transport

        if len(self.tests_available()) != len(set(self.tests_available())):
            raise RuntimeError(f"Test names for part {part.name} are not unique")

        self.debug = debug

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def dut_setup(self):
        self.tr.send([Tester.CMD_DUT_SETUP, self.part.package_type,  self.part.pincount])

        if self.debug:
            print("Pin roles:")

        for num, pin in sorted(self.part.pins.items()):
            if self.debug:
                print(f" {num:-2}: {pin.role_name}")
            self.tr.send([pin.role])

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT setup failed")

    def test_setup(self, test):
        self.tr.send([Tester.CMD_TEST_SETUP, test.type, test.subtype])

        data = [
            1 if i in test.pins else 0
            for i in reversed(sorted(self.part.pins))
        ]
        if self.debug:
            print(f"Pin used by the test: {data}")
        self.tr.send(BV(data))

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if self.debug:
            print(f"Test vectors ({len(test.body)}):")
            for v in test.vectors:
                print(f" {v}")

        assert len(test.body) <= Tester.MAX_LEN

        self.tr.send([Tester.CMD_VECTORS_LOAD])
        self.tr.send(BV.int(len(test.body), 16))

        if self.debug:
            print("Binary vectors:")

        for v in test.vectors:
            data = v.by_pins(reversed(sorted(self.part.pins)))
            if self.debug:
                print(f" {data}")
            self.tr.send(BV(data))

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Vectors load failed")

    def run(self, loop_pow):
        assert loop_pow < 16

        self.tr.send([Tester.CMD_RUN, loop_pow])

        start = time.time()
        result = self.tr.recv()
        elapsed = time.time() - start

        return result, elapsed

    def exec_test(self, test, loop_pow):
        self.dut_setup()
        self.test_setup(test)
        self.vectors_load(test)
        res = self.run(loop_pow)
        if self.debug:
            print(f"Bytes sent: {self.tr.bytes_sent}, received: {self.tr.bytes_received}")
        return res
