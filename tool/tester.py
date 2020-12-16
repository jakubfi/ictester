import serial
from prototypes import (Pin)


class Tester:
    CMD_SETUP = 0b00000000
    CMD_UPLOAD = 0b00100000
    CMD_RUN = 0b01000000
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

    def send(self, b):
        if self.debug:
            print("<- {:08b} {}".format(b, b))
        data = bytes([b])
        self.s.write(data)

    def recv(self):
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
        input_pins = [
            False if not p else self.part.pins[p-1].role == Pin.INPUT
            for p in Tester.pin_map[self.part.package_name]
        ]
        if self.debug:
            print("Input pins: {}".format(input_pins))
            print("Used pins: {}".format(used_pins))

        self._setup(used_pins, input_pins)

    def _setup(self, used, inputs):
        used = self.tf_to_bin(used)
        inputs = self.tf_to_bin(inputs)
        self.send(Tester.CMD_SETUP)
        for shift in [16, 8, 0]:
            self.send((used >> shift) & 0xff)
            self.send((inputs >> shift) & 0xff)
        if self.recv() != Tester.RES_OK:
            raise RuntimeError("Setup failed")

    def deconfigure(self):
        self.send(Tester.CMD_SETUP)
        for shift in range(0, 6):
            self.send(0)
        if self.recv() != Tester.RES_OK:
            raise RuntimeError("Deconfiguration failed")

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def upload(self, test_name):
        test = self.part.get_test(test_name)

        self.send(Tester.CMD_UPLOAD)
        self.send(test.type)
        self.send(len(test.body))

        for v in test.body:
            v_pin = self.part.vector_by_pins(v)
            # translate pin-order test vector to a port-ordered vector
            v_port = self.tf_to_bin([
                0 if not p else v_pin[p-1]
                for p in Tester.pin_map[self.part.package_name]
            ])
            if self.debug:
                print("Input vector: {}".format(v))
                print("Pin-ordered vector: {}".format(v_pin))
                print("Port-ordered vector: {:024b}".format(v_port))
            for shift in [16, 8, 0]:
                self.send((v_port >> shift) & 0xff)

        if self.recv() != Tester.RES_OK:
            raise RuntimeError("Upload failed")

    def run(self, test_name, loop_pow):
        assert loop_pow < 16
        self.upload(test_name)
        self.send(Tester.CMD_RUN)
        self.send(loop_pow)
        return self.recv()
