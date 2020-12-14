import serial
from prototypes import Pin


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

    pin_map_dip14 = [
        0, 0, 8, 9, 10, 11, 12, 13,  # port A
        0, 0, 0, 0,  0,  0,  0,  0,  # port B
        0, 0, 6, 5,  4,  3,  2,  1,  # port C
    ]

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
        self.used = self.tf_to_bin([
            False if not p else self.part.pins[p-1].role not in [Pin.POWER, Pin.NC]
            for p in Tester.pin_map_dip14
        ])
        self.inputs = self.tf_to_bin([
            False if not p else self.part.pins[p-1].role == Pin.INPUT
            for p in Tester.pin_map_dip14
        ])

        self.setup()

    def setup(self):
        self.write(Tester.CMD_SETUP)
        for shift in [16, 8, 0]:
            self.write((self.used >> shift) & 0xff)
            self.write((self.inputs >> shift) & 0xff)
        if self.read() != Tester.RES_OK:
            raise RuntimeError("Setup failed")

    def tests_available(self):
        return [t for t in self.part.tests.keys()]

    def upload(self, test_name):
        test_body, test_seq = self.part.tests[test_name]

        self.write(Tester.CMD_UPLOAD)
        if test_seq:
            if self.debug:
                print("Sequential test")
            self.write(Tester.TYPE_SEQ)
        else:
            if self.debug:
                print("Combinatorial test")
            self.write(Tester.TYPE_COMB)

        self.write(len(test_body))

        for v in test_body:
            if self.debug:
                print("User vector: {}".format(v))
            test_vector = self.part.vector_by_pins(v)
            if self.debug:
                print("Pin vector: {}".format(test_vector))
            # translate pin-order test vector to a port-order vector
            test_vector_out = self.tf_to_bin([
                False if not p else test_vector[p-1]
                for p in Tester.pin_map_dip14
            ])
            if self.debug:
                print("Port vector: {:024b}".format(test_vector_out))
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
