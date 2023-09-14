import time
from prototypes import Test
from binvec import BV


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
    RESP_TIMING_FAIL = 133

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
        cfg_count = 0
        for pin in self.part.pins.values():
            if len(pin.zif_func) > cfg_count:
                cfg_count = len(pin.zif_func)
        assert 5 > cfg_count > 0
        self.tr.send([Tester.CMD_DUT_SETUP, self.part.package_type, self.part.pincount, cfg_count])

        if self.debug:
            print(f"DUT pin definitions, {cfg_count} configuration(-s) available:")

        for cfgnum in range(0, cfg_count):
            if self.debug:
                print(f"Configuration {cfgnum}:")
            for num, pin in sorted(self.part.pins.items()):
                try:
                    pin_func = pin.zif_func[cfgnum]
                except IndexError:
                    pin_func = pin.zif_func[0]
                if self.debug:
                    print(f'{num:-3} {pin.name:6} {pin.role.name:5} ZIF {pin_func.name}')
                self.tr.send([pin_func.value])

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT setup failed")

    def dut_connect(self, cfgnum):
        if self.debug:
            print("---- DUT CONNECT ----------------------------------")
        self.tr.send([Tester.CMD_DUT_CONNECT, cfgnum])
        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("DUT connect failed")

    def dut_disconnect(self):
        if self.debug:
            print("---- DUT DISCONNECT -------------------------------")
        self.tr.send([Tester.CMD_DUT_DISCONNECT])
        if self.tr.recv() != Tester.RESP_OK:
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

        self.tr.send([Tester.CMD_TEST_SETUP, test.cfgnum, test.type, *params])

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

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if self.debug:
            print("---- VECTORS LOAD ---------------------------------")
        if self.debug:
            print(f"Test vectors ({len(test.vectors)}):")
            for v in test.vectors:
                print(f" {v}")

        assert len(test.vectors) <= Tester.MAX_VECTORS

        self.tr.send([Tester.CMD_VECTORS_LOAD])
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

        if self.tr.recv() != Tester.RESP_OK:
            raise RuntimeError("Vectors load failed")

    def run(self, loops, test):
        if self.debug:
            print("---- RUN ------------------------------------------")
        assert 1 <= loops <= 0xffff

        self.tr.send([Tester.CMD_RUN])
        self.tr.send_16le(loops)

        start = time.time()
        result = self.tr.recv()
        elapsed = time.time() - start
        failed_vector_num = None
        failed_zif_vector = None

        # Read failed vector data for LOGIC tests (natural DUT pin order)
        if test.type == Test.LOGIC and result == Tester.RESP_FAIL:
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
