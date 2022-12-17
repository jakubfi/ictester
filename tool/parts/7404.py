from prototypes import (PackageDIP14, Pin, Test)

class Part7404(PackageDIP14):
    name = "7404"
    desc = "Hex inverters"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1Y", Pin.OUT),
        3: Pin("2A", Pin.IN),
        4: Pin("2Y", Pin.OUT),
        5: Pin("3A", Pin.IN),
        6: Pin("3Y", Pin.OUT),
        8: Pin("6Y", Pin.OUT),
        9: Pin("6A", Pin.IN),
        10: Pin("5Y", Pin.OUT),
        11: Pin("5A", Pin.IN),
        12: Pin("4Y", Pin.OUT),
        13: Pin("4A", Pin.IN),
    }
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            ttype=Test.COMB,
            body=Test.binary_fun_gen(6, 1, lambda a: a, inverted=True)
        )
    ]