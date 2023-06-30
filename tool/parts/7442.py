from binvec import BV
from prototypes import (PackageDIP16, Pin, Test)

class Part7442(PackageDIP16):
    name = "7442"
    desc = "4-line BCD to 10-line decimal decoders"
    pin_cfg = {
        1: Pin("0", Pin.OUT),
        2: Pin("1", Pin.OUT),
        3: Pin("2", Pin.OUT),
        4: Pin("3", Pin.OUT),
        5: Pin("4", Pin.OUT),
        6: Pin("5", Pin.OUT),
        7: Pin("6", Pin.OUT),
        9: Pin("7", Pin.OUT),
        10: Pin("8", Pin.OUT),
        11: Pin("9", Pin.OUT),
        12: Pin("D", Pin.IN),
        13: Pin("C", Pin.IN),
        14: Pin("B", Pin.IN),
        15: Pin("A", Pin.IN),
    }

    test_async = Test("Asynchronous operation", Test.COMB,
        inputs=[12, 13, 14, 15],
        outputs=[11, 10, 9, 7, 6, 5, 4, 3, 2, 1],
        body=[[BV.int(i, 4),  ~BV.bit(i, 10)] for i in range(0, 16)]
    )

    tests = [test_async]
