import serial
from prototypes import Pin


class Tester:
    CMD_SETUP = 0
    CMD_UPLOAD = 1
    CMD_RUN = 2
    RES_OK = 0
    RES_ERR = 1
    RES_PASS = 2
    RES_FAIL = 3
    MAX_LEN = 1024

    pin_map = {
        "DIP14": [
            0,  0,  6,  5,  4,  3, 2, 1,  # port A[7..0]
            0,  0,  0,  0,  0,  0, 0, 0,  # port B[7..0]
            0,  0, 13, 12, 11, 10, 9, 8,  # port C[7..0]
        ],
        "DIP14, VCC@pin5": [
            0, 14, 13, 12, 11,  9,  8,  0,  # port A[7..0]
            0,  0,  0,  0,  0,  0,  0,  0,  # port B[7..0]
            0,  1,  2,  3,  4,  6,  7,  0,  # port C[7..0]
        ],
        "DIP14, VCC@pin4": [
            0,  0, 14, 13, 12, 10,  9,  8,  # port A[7..0]
            0,  0,  0,  0,  0,  0,  0,  0,  # port B[7..0]
            0,  0,  1,  2,  3,  5,  6,  7,  # port C[7..0]
        ],
        "DIP16": [
            0,  9, 10, 11, 12, 13, 14, 15,  # port A[7..0]
            0,  0,  0,  0,  0,  0,  0,  0,  # port B[7..0]
            0,  1,  2,  3,  4,  5,  6,  7,  # port C[7..0]
        ],
        "DIP16 rotated, VCC@pin8": [
            0,  1,  2,  3,  4,  5,  6,  7,  # port A[7..0]
            0,  0,  0,  0,  0,  0,  0,  0,  # port B[7..0]
            0,  9, 10, 11, 12, 13, 14, 15,  # port C[7..0]
        ],
        "DIP16, VCC@pin5": [
            0, 16, 15, 14, 13, 11, 10,  9,  # port A[7..0]
            0,  0,  0,  0,  0,  0,  0,  0,  # port B[7..0]
            0,  1,  2,  3,  4,  6,  7,  8,  # port C[7..0]
        ],
        "DIP24": [
            8,   7,  6,  5,  4,  3,  2,  1,  # port A[7..0]
            0,   0, 21, 22, 23, 11, 10,  9,  # port B[7..0]
            20, 19, 18, 17, 16, 15, 14, 13,  # port C[7..0]
        ],
    }

    def __init__(self, part_class, port, speed, debug=False, serial_debug=False):
        self.part = part_class()
        # accept either test list or gen_tests() method
        try:
            self.part.gen_tests()
        except AttributeError:
            assert self.part.tests

        # no duplicate names allowed
        assert len(self.tests_available()) == len(set(self.tests_available()))

        self.debug = debug
        self.serial_debug = serial_debug
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
        if self.serial_debug:
            print("<- {:08b} {}".format(b, b))
        data = bytes([b])
        self.s.write(data)

    def recv(self):
        b = ord(self.s.read(1))
        if self.serial_debug:
            print("-> {:08b} {}".format(b, b))
        return b

    def v2bin(self, tf):
        """
        translate a [True/False] vector to its binary representation
        """
        b = 0
        bit_length = len(tf)
        for i in range(0, bit_length):
            b |= int(tf[i]) << (bit_length-i-1)
        return b

    def tests_available(self):
        return [t.name for t in self.part.tests]

    def get_used_pins(self, test):
        all_pins = test.inputs + test.outputs
        return [
            0 if not p else (1 if p in all_pins else 0)
            for p in Tester.pin_map[self.part.package_name]
        ]

    def get_input_pins(self, test):
        return [
            0 if not p else (1 if p in test.inputs else 0)
            for p in Tester.pin_map[self.part.package_name]
        ]

    def get_pullup_pins(self, test):
        return [
            0 if not p else (1 if self.part.pins[p-1].role == Pin.OC else 0)
            for p in Tester.pin_map[self.part.package_name]
        ]

    def setup(self, test):
        used = self.v2bin(self.get_used_pins(test))
        inputs = self.v2bin(self.get_input_pins(test))
        pullup = self.v2bin(self.get_pullup_pins(test))
        if self.debug:
            print("  Used pins: {:024b}".format(used))
            print(" Input pins: {:024b}".format(inputs))
            print("Pullup pins: {:024b}".format(pullup))

        self.send(Tester.CMD_SETUP)
        for shift in [16, 8, 0]:
            self.send((used >> shift) & 0xff)
            self.send((inputs >> shift) & 0xff)
            self.send((pullup >> shift) & 0xff)
        if self.recv() != Tester.RES_OK:
            raise RuntimeError("Setup failed")

    def get_pinvalue(self, pins, vals, pin):
        return 0 if pin not in pins else vals[pins.index(pin)]

    def vector_by_port(self, pins, vals):
        return [
            0 if not pin else self.get_pinvalue(pins, vals, pin)
            for pin in Tester.pin_map[self.part.package_name]
        ]

    def sequentialize(self, v):
        i = v[0]
        o = v[1]
        return [
            [[x if x in [0, 1] else 0 if x == '+' else 1 for x in i], o],
            [[x if x in [0, 1] else 1 if x == '+' else 0 for x in i], o],
        ]

    def upload(self, test):
        if test.type == test.COMB:
            body = test.body
        else:
            body = []
            for t in test.body:
                body.extend(self.sequentialize(t))

        if self.debug:
            print("Test len: {}".format(len(body)))

        assert len(body) <= Tester.MAX_LEN

        self.send(Tester.CMD_UPLOAD)
        self.send(test.type)
        self.send(test.subtype)
        self.send(len(body) >> 8)
        self.send(len(body) & 0xff)

        all_pins = test.inputs + test.outputs
        for v in body:
            v_port = self.vector_by_port(all_pins, v[0] + v[1])
            v_port_bin = self.v2bin(v_port)
            if self.debug:
                print("Input vector: {}".format(v))
                print("Port-ordered vector: {}".format(v_port))
                print("Port-ordered vector: {:024b}".format(v_port_bin))
            for shift in [16, 8, 0]:
                self.send((v_port_bin >> shift) & 0xff)

        if self.recv() != Tester.RES_OK:
            raise RuntimeError("Upload failed")

    def run(self, test, loop_pow):
        assert loop_pow < 16

        self.setup(test)
        self.upload(test)
        self.send(Tester.CMD_RUN)
        self.send(loop_pow)
        return self.recv()
