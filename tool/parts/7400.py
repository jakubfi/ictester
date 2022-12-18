from prototypes import (PackageDIP14, Pin, Test)

class Part7400(PackageDIP14):
    name = "7400"
    desc = "Quad 2-input positive-NAND gates"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1B", Pin.IN),
        3: Pin("1Y", Pin.OUT),
        4: Pin("2A", Pin.IN),
        5: Pin("2B", Pin.IN),
        6: Pin("2Y", Pin.OUT),
        8: Pin("3Y", Pin.OUT),
        9: Pin("3A", Pin.IN),
        10: Pin("3B", Pin.IN),
        11: Pin("4Y", Pin.OUT),
        12: Pin("4A", Pin.IN),
        13: Pin("4B", Pin.IN),
    }

    tests = [
        Test("Complete logic", Test.COMB,
            inputs=[1, 2, 4, 5, 10, 9, 13, 12],
            outputs=[3, 6, 8, 11],
            body=Test.binary_fun_gen(4, 2, lambda a, b: a & b, inverted=True)
        )
    ]
