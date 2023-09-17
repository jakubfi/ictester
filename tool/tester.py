import time
from enum import Enum
from prototypes import Test
from binvec import BV

Cmd = Enum("Cmd",
    names=[
        ("HELLO", 1),
        ("DUT_SETUP", 2),
        ("DUT_CONNECT", 3),
        ("TEST_SETUP", 4),
        ("VECTORS_LOAD", 5),
        ("RUN", 6),
        ("DUT_DISCONNECT", 7),
    ]
)

Resp = Enum("Response",
    names=[
        ("HELLO", 128),
        ("OK", 129),
        ("PASS", 130),
        ("FAIL", 131),
        ("ERR", 132),
        ("TIMING_FAIL", 133),
    ]
)

class Tester:

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
        self.debug = debug

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def dut_setup(self):
        if self.debug:
            print("---- DUT SETUP ------------------------------------")
        self.tr.send([Cmd.DUT_SETUP.value])
        self.tr.send(self.part)
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT setup failed")

    def dut_connect(self, cfgnum):
        if self.debug:
            print("---- DUT CONNECT ----------------------------------")
        self.tr.send([Cmd.DUT_CONNECT.value, cfgnum])
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT connect failed")

    def dut_disconnect(self):
        if self.debug:
            print("---- DUT DISCONNECT -------------------------------")
        self.tr.send([Cmd.DUT_DISCONNECT.value])
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT disconnect failed")

    def test_setup(self, test, delay):
        if self.debug:
            print("---- TEST SETUP -----------------------------------")
        params = test.params
        if delay is not None:
            if test.type == Test.LOGIC:
                delay_val = round(delay/0.2)
                params[0] = delay_val & 0xff
                params[1] = delay_val >> 8

        self.tr.send([Cmd.TEST_SETUP.value, test.cfgnum, test.type, *params])

        data = [
            1 if i in test.pins else 0
            for i in reversed(sorted(self.part.pins))
        ]
        if self.debug:
            print(f"Configuration used: {test.cfgnum}")
            print(f"Test pin usage map: {data}")
            print(f"DUT inputs: {test.inputs}")
            print(f"DUT outputs: {test.outputs}")
        self.tr.send_bitarray(data)

        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if self.debug:
            print("---- VECTORS LOAD ---------------------------------")
        if self.debug:
            print(f"Test vectors ({len(test.vectors)}):")
            for v in test.vectors:
                print(f" {v}")

        assert len(test.vectors) <= Tester.MAX_VECTORS

        self.tr.send([Cmd.VECTORS_LOAD.value])
        self.tr.send_16le(len(test.vectors))

        if self.debug:
            print("Binary vectors:")

        for v in test.vectors:
            data = v.by_pins(sorted(self.part.pins))
            # If output is empty, that means DUT outputs shouldn't be checked
            # Protocol marks such case with "1" on VCC position
            if not v.output:
                for vcc in self.part.vcc:
                    data[vcc-1] = 1

            data = list(reversed(data))

            if self.debug:
                check = " NC" if not v.output else ""
                print(f" {list(map(int, data))}{check}")

            self.tr.send_bitarray(data)

        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("Vectors load failed")

    def run(self, loops, test):
        if self.debug:
            print("---- RUN ------------------------------------------")
        assert 1 <= loops <= 0xffff

        self.tr.send([Cmd.RUN.value])
        self.tr.send_16le(loops)

        start = time.time()
        result = self.tr.recv()
        elapsed = time.time() - start
        failed_vector_num = None
        failed_pin_vector = None

        # Read failed vector data for LOGIC tests (natural DUT pin order)
        if test.type == Test.LOGIC and result == Resp.FAIL.value:
            failed_vector_num = self.tr.recv_16le()
            failed_pin_vector = [*BV.int(self.tr.recv(), 8).reversed()]
            failed_pin_vector.extend([*BV.int(self.tr.recv(), 8).reversed()])
            if self.part.pincount > 16:
                failed_pin_vector.extend([*BV.int(self.tr.recv(), 8).reversed()])

        return result, elapsed, failed_vector_num, failed_pin_vector

    def exec_test(self, test, loops, delay):
        self.test_setup(test, delay)
        if test.type == Test.LOGIC:
            self.vectors_load(test)
        res = self.run(loops, test)
        if self.debug:
            print(f"Bytes sent: {self.tr.bytes_sent}, received: {self.tr.bytes_received}")
        return res
