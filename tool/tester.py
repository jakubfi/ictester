import time
import logging
from enum import Enum
from prototypes import (Test, TestType)
from binvec import BV

logger = logging.getLogger('ictester')

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
        ("TIMING_ERROR", 133),
        ("SKIP", 9999999)  # not a part of the protocol
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

    def __init__(self, part, transport):
        self.part = part
        self.tr = transport
        self.failed_vector_num = None
        self.failed_pin_vector = None
        self.passed = 0
        self.warning = 0
        self.failed = 0

    def dut_setup(self):
        logger.info("---- DUT SETUP ------------------------------------")
        self.tr.send([Cmd.DUT_SETUP.value])
        self.tr.send(self.part)
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT setup failed")

    def dut_connect(self, cfgnum):
        logger.info("---- DUT CONNECT ----------------------------------")
        self.tr.send([Cmd.DUT_CONNECT.value, cfgnum])
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT connect failed")

    def dut_disconnect(self):
        logger.info("---- DUT DISCONNECT -------------------------------")
        self.tr.send([Cmd.DUT_DISCONNECT.value])
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("DUT disconnect failed")

    def test_setup(self, test):
        logger.info("\n---- TEST SETUP -----------------------------------")
        self.tr.send([Cmd.TEST_SETUP.value])
        self.tr.send(test)
        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("Test setup failed")

    def vectors_load(self, test):
        if logger.isEnabledFor(logging.INFO):
            logger.info("---- VECTORS LOAD ---------------------------------")
            logger.info("Test vectors (%s)", len(test.vectors))
            for v in test.vectors:
                logger.info(v)

        assert len(test.vectors) <= Tester.MAX_VECTORS

        self.tr.send([Cmd.VECTORS_LOAD.value])
        self.tr.send_16le(len(test.vectors))

        logger.info("Binary vectors:")

        for v in test.vectors:
            self.tr.send(v)

        if self.tr.recv() != Resp.OK.value:
            raise RuntimeError("Vectors load failed")

    def run(self, loops, test):
        logger.info("---- RUN ------------------------------------------")
        assert 1 <= loops <= 0xffff

        self.tr.send([Cmd.RUN.value])
        self.tr.send_16le(loops)

        start = time.time()
        resp = Resp(self.tr.recv())
        elapsed = time.time() - start

        if resp == Resp.PASS:
            self.passed += 1
        elif resp == Resp.TIMING_ERROR:
            self.warning += 1
        else:
            self.failed += 1

        # Read failed vector data for LOGIC tests (natural DUT pin order)
        if test.type == TestType.LOGIC and resp == Resp.FAIL:
            self.failed_vector_num = self.tr.recv_16le()
            self.failed_pin_vector = [*BV.int(self.tr.recv(), 8).reversed()]
            self. failed_pin_vector.extend([*BV.int(self.tr.recv(), 8).reversed()])
            if self.part.pincount > 16:
                self.failed_pin_vector.extend([*BV.int(self.tr.recv(), 8).reversed()])

        return resp, elapsed

    def get_failed_vector(self):
        return self.failed_vector_num, self.failed_pin_vector

    def exec_test(self, test, loops, delay):
        test.attach_part(self.part)
        if delay is not None:
            test.set_delay(delay)
        self.test_setup(test)
        if test.type == TestType.LOGIC:
            self.vectors_load(test)
        res = self.run(loops, test)
        logger.info("Bytes sent: %s, received: %s", self.tr.bytes_sent, self.tr.bytes_received)
        return res
