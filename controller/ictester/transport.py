import logging
import serial
from ictester.binvec import BV
from struct import (pack, unpack)

logger = logging.getLogger('ictester')

class Transport:
    def __init__(self, port, speed):
        self._s = None
        self.port = port
        self.speed = speed
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
        self.bytes_sent += len(b)
        self.s.write(pack("<H", len(b)))
        logger.log(18, "<- (%s bytes) %s", len(b), bytes(b).hex(" "))
        self.s.write(b)

    def recv(self):
        size = unpack("<H", self.s.read(2))[0]
        payload = self.s.read(size)
        logger.log(18, "-> (%s bytes) %s", size, payload.hex(" "))
        self.bytes_received += 2 + len(payload)
        return payload
