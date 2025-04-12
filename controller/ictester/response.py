from enum import Enum

class ICTesterException(Exception):
    pass

RespType = Enum("Response",
    names=[
        ("HELLO", 128),
        ("OK", 129),
        ("PASS", 130),
        ("FAIL", 131),
        ("ERR", 132),
        ("TIMING_ERROR", 133),
    ]
)

error_message = {
    0:  "Error code was not set (likely a software bug)",
    1:  "Unknown command",
    2:  "Command didn't fit in the receive buffer",
    3:  "CRC transmission error detected",
    4:  "(unknown)",
    5:  "Unsupported package type",
    6:  "Unsupported pin count",
    7:  "Unknown pin function",
    8:  "Bad pin function combination (eg. VCC+GND)",
    9:  "DUT not configured",
    10: "Unsupported test type",
    11: "(unknown)",
    12: "Wrong number of test vectors (<1 or too many)",
    13: "Wrong pin configuration count",
    14: "Wrong pin configuration number (config not set)",
    15: "(unknown)",
    16: "Function not available for a pin",
    17: "No pin configuration active",
    18: "Selected chip type is unknown",
    19: "No such test for selected chip",
    20: "Overcurrent when connecting the DUT",
}

class Response:
    def __init__(self, tr):
        data = tr.recv()
        self.payload = None
        self.reason = None
        self.response = RespType(data[0])

        if self.response == RespType.ERR:
            error_code = int(data[1])
            self.payload = data[2:]
        else:
            self.payload = data[1:]
