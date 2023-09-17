import serial
from binvec import BV


class Transport:
    def __init__(self, port, speed, debug=False):
        self._s = None
        self.port = port
        self.speed = speed
        self.debug = debug
        self.bytes_sent = 0
        self.bytes_received = 0

        self.s = serial.Serial(
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

    def send(self, b):
        b = bytes(b)
        if self.debug:
            data = [f"{x:08b} ({chr(x)})" for x in b]
            print(f"<- {data}")
        self.s.write(b)
        self.bytes_sent += len(b)

    def send_16le(self, val):
        self.send(val.to_bytes(2, 'little'))

    def recv(self):
        b = ord(self.s.read(1))
        self.bytes_received += 1
        if self.debug:
            print(f"-> {b:>08b} {b}")
        return b

    def recv_16le(self):
        return self.recv() + (self.recv() << 8)
