import serial
from prototypes import (Pin, Test)


class Tester:
    CMD_SETUP = 0b00000000
    CMD_UPLOAD = 0b00100000
    CMD_RUN = 0b01000000
    TYPE_COMB = 0
    TYPE_SEQ = 1
    RES_OK = 0
    RES_ERR = 1
    RES_PASS = 2
    RES_FAIL = 3

    pin_map = {
        "DIP14": [
            0, 0, 6,  5,  4,  3, 2, 1,   # port A
            0, 0, 0,  0,  0,  0, 0, 0,   # port B
            0, 0, 13, 12, 11, 10, 9, 8,  # port C
        ],
        "DIP16": [
            0, 9, 10, 11, 12, 13, 14, 15,  # port A
            0, 0, 0,  0,  0,  0,  0,  0,   # port B
            0, 1, 2,  3,  4,  5,  6,  7,   # port C
        ],
        "DIP24": [
            8,  7,  6,  5,  4,  3,  2,  1,   # port A
            0,  0,  21, 22, 23, 11, 10, 9,   # port B
            20, 19, 18, 17, 16, 15, 14, 13,  # port C
        ],
    }

    def __init__(self, port, speed, debug=False):
        self.part = None
        self.debug = debug
        self.s = serial.Serial(
            port,
            baudrate=speed,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=None,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )

    def write(self, b):
        if self.debug:
            print("<- {:08b} {}".format(b, b))
        data = bytes([b])
        self.s.write(data)

    def read(self):
        b = ord(self.s.read(1))
        if self.debug:
            print("-> {:08b} {}".format(b, b))
        return b

    def tf_to_bin(self, tf):
        """
        translate [True/False] vector to its binary representation
        """
        b = 0
        bit_length = len(tf)
        for i in range(0, bit_length):
            b |= int(tf[i]) << (bit_length-i-1)
        return b

    def load_part(self, part_class):
        self.part = part_class()
        used_pins = [
            False if not p else self.part.pins[p-1].role not in [Pin.POWER, Pin.NC]
            for p in Tester.pin_map[self.part.package_name]
        ]
        if self.debug:
            print("Used pins: {}".format(used_pins))
        self.used = self.tf_to_bin(used_pins)
        input_pins = [
            False if not p else self.part.pins[p-1].role == Pin.INPUT
            for p in Tester.pin_map[self.part.package_name]
        ]
        if self.debug:
            print("Input pins: {}".format(input_pins))
        self.inputs = self.tf_to_bin(input_pins)

        self.setup()

    def setup(self):
        self.write(Tester.CMD_SETUP)
        for shift in [16, 8, 0]:
            self.write((self.used >> shift) & 0xff)
            self.write((self.inputs >> shift) & 0xff)
        if self.read() != Tester.RES_OK:
            raise RuntimeError("Setup failed")

    def deconfigure(self):
        self.write(Tester.CMD_SETUP)
        for shift in range(0, 6):
            self.write(0)
        if self.read() != Tester.RES_OK:
            raise RuntimeError("Deconfiguration failed")

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def upload(self, test_name):
        test = self.part.get_test(test_name)

        self.write(Tester.CMD_UPLOAD)
        if test.type == Test.SEQ:
            if self.debug:
                print("Sequential test")
            self.write(Tester.TYPE_SEQ)
        else:
            if self.debug:
                print("Combinatorial test")
            self.write(Tester.TYPE_COMB)

        self.write(len(test.body))

        for v in test.body:
            if self.debug:
                print("User vector: {}".format(v))
            test_vector = self.part.vector_by_pins(v)
            if self.debug:
                print("Pin vector: {}".format(test_vector))
            # translate pin-order test vector to a port-order vector
            test_vector_port = [
                0 if not p else test_vector[p-1]
                for p in Tester.pin_map[self.part.package_name]
            ]
            test_vector_out = self.tf_to_bin(test_vector_port)
            if self.debug:
                print("Port vector: {}".format(test_vector_port))
                print("Port vector (bin): {:024b}".format(test_vector_out))
            for shift in [16, 8, 0]:
                self.write((test_vector_out >> shift) & 0xff)

        if self.read() != Tester.RES_OK:
            raise RuntimeError("Upload failed")

    def run(self, test_name, loop_pow):
        assert loop_pow < 16
        self.upload(test_name)
        self.write(Tester.CMD_RUN)
        self.write(loop_pow)
        return self.read()
