from ictester.binvec import BV
from ictester.part import (PackageDIP16, Pin, PinType)
from ictester.test import TestLogic

class Part7442(PackageDIP16):
    name = "7442"
    desc = "4-line BCD to 10-line decimal decoders"
    pin_cfg = {
        1: Pin("0", PinType.OUT),
        2: Pin("1", PinType.OUT),
        3: Pin("2", PinType.OUT),
        4: Pin("3", PinType.OUT),
        5: Pin("4", PinType.OUT),
        6: Pin("5", PinType.OUT),
        7: Pin("6", PinType.OUT),
        9: Pin("7", PinType.OUT),
        10: Pin("8", PinType.OUT),
        11: Pin("9", PinType.OUT),
        12: Pin("D", PinType.IN),
        13: Pin("C", PinType.IN),
        14: Pin("B", PinType.IN),
        15: Pin("A", PinType.IN),
    }

    test_async = TestLogic("Asynchronous operation",
        inputs=[12, 13, 14, 15],
        outputs=[11, 10, 9, 7, 6, 5, 4, 3, 2, 1],
        body=[[BV.int(i, 4),  ~BV.bit(i, 10)] for i in range(0, 2**4)]
    )

    tests = [test_async]
