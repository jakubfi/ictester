from prototypes import (PackageDIP14, Pin, Test)

class Part74H61(PackageDIP14):
    name = "74H61"
    desc = "Triple 3-input expanders"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1B", Pin.IN),
        3: Pin("1C", Pin.IN),
        4: Pin("2A", Pin.IN),
        5: Pin("2B", Pin.IN),
        6: Pin("2C", Pin.IN),
        8: Pin("2X", Pin.OC),
        9: Pin("1X", Pin.OC),
        10: Pin("3X", Pin.OC),
        11: Pin("3A", Pin.IN),
        12: Pin("3B", Pin.IN),
        13: Pin("3C", Pin.IN),
    }

    test_async = Test("Asynchronous operation", Test.COMB,
        inputs=[1, 2, 3,  4, 5, 6,  11, 12, 13],
        outputs=[9, 8, 10],
        loops = 64,
        body = Test.binary_fun_gen(3, 3, lambda a, b: a & b, inverted=True)
    )

    tests = [test_async]
