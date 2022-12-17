from prototypes import (PackageDIP14, Pin, Test)

class Part7402(PackageDIP14):
    name = "7402"
    desc = "Quad 2-input positive-NOR gates"
    pin_cfg = {
        1: Pin("1Y", Pin.OUT),
        2: Pin("1A", Pin.IN),
        3: Pin("1B", Pin.IN),
        4: Pin("2Y", Pin.OUT),
        5: Pin("2A", Pin.IN),
        6: Pin("2B", Pin.IN),
        8: Pin("3A", Pin.IN),
        9: Pin("3B", Pin.IN),
        10: Pin("3Y", Pin.OUT),
        11: Pin("4A", Pin.IN),
        12: Pin("4B", Pin.IN),
        13: Pin("4Y", Pin.OUT),
    }
    tests = [
        Test(
            name="Complete logic",
            inputs=[2, 3, 5, 6, 8, 9, 11, 12],
            outputs=[1, 4, 10, 13],
            ttype=Test.COMB,
            body=Test.binary_fun_gen(4, 2, lambda a, b: a | b, inverted=True)
        )
    ]
