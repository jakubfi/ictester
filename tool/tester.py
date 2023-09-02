import time


class Tester:
    CMD_HELLO = 1
    CMD_DUT_SETUP = 2
    CMD_DUT_CONNECT = 3
    CMD_TEST_SETUP = 4
    CMD_VECTORS_LOAD = 5
    CMD_RUN = 6
    CMD_DUT_DISCONNECT = 7

    RESP_HELLO = 128
    RESP_OK = 129
    RESP_PASS = 130
    RESP_FAIL = 131
    RESP_ERR = 132

    error_strings = {
        0: "Error code was not set",
        1: "Unknown command",
        2: "Missing DUT setup",
        3: "No test set",
        4: "No vectors loaded",
        5: "Unsupported package type",
        6: "Unsupported pin count",
        7: "Unknown pin function",
        8: "Bad pin function combination",
        9: "Unsupported pin setup",
        10: "Unsupported test type",
        11: "Bad test parameters",
        12: "Wrong number of test vectors",
    }

    MAX_VECTORS = 1024

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
            print("DUT pin definitions:")

        for num, pin in sorted(self.part.pins.items()):
            if self.debug:
                print(f'{num:-3} {pin.name:6} {pin.role.name:5} ZIF {pin.zif_func.name}')
            self.tr.send([pin.zif_func.value])

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT setup failed")

    def dut_connect(self):
        self.tr.send([Tester.CMD_DUT_CONNECT])
        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT connect failed")

    def dut_disconnect(self):
        self.tr.send([Tester.CMD_DUT_DISCONNECT])
        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT disconnect failed")

    def test_setup(self, test):
        self.tr.send([Tester.CMD_TEST_SETUP, test.type, *test.params])

        data = [
            1 if i in test.pins else 0
            for i in reversed(sorted(self.part.pins))
        ]
        if self.debug:
            print(f"Test pin usage map: {data}")
            print(f"DUT inputs: {test.inputs}")
            print(f"DUT outputs: {test.outputs}")
        self.tr.send_bitarray(data)

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if self.debug:
            print(f"Test vectors ({len(test.body)}):")
            for v in test.vectors:
                print(f" {v}")

        assert len(test.body) <= Tester.MAX_VECTORS

        self.tr.send([Tester.CMD_VECTORS_LOAD])
        self.tr.send_16le(len(test.body))

        if self.debug:
            print("Binary vectors:")

        for v in test.vectors:
            data = v.by_pins(reversed(sorted(self.part.pins)))
            if self.debug:
                print(f" {data}")
            self.tr.send_bitarray(data)

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Vectors load failed")

    def run(self, loops, delay):
        assert 1 <= loops <= 0xffff

        if self.debug:
            print(f"Running test: {loops} loops, {delay} us output read delay")
        self.tr.send([Tester.CMD_RUN])
        self.tr.send_16le(loops)
        self.tr.send_16le(round(delay//0.2)) # unit is 0.2us

        start = time.time()
        result = self.tr.recv()
        elapsed = time.time() - start

        return result, elapsed

    def exec_test(self, test, loops, delay):
        self.test_setup(test)
        self.vectors_load(test)
        res = self.run(loops, delay if delay is not None else self.part.read_delay_us)
        if self.debug:
            print(f"Bytes sent: {self.tr.bytes_sent}, received: {self.tr.bytes_received}")
        return res
