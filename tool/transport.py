import logging
import serial
from binvec import BV
from struct import pack

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
        self.s.write(pack("<H", len(b)))
        logger.debug("<- (%s bytes) %s", len(b), bytes(b).hex(" "))
        self.s.write(b)
        self.bytes_sent += len(b)

    def recv(self, count=1):
        b = self.s.read(count)
        logger.debug("-> %s", b.hex(" "))
        if count == 1:
            b = ord(b)  # temporary backwards compatibility
        self.bytes_received += count
        return b
