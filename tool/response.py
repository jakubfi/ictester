from enum import Enum

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

class Response:
    def __init__(self, tr):
        data = tr.recv()
        self.response = RespType(data[0])
        self.payload = data[1:]
