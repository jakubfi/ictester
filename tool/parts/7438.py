from prototypes import (Pin, partimport)

class Part7438(partimport("7400")):
    name = "7438"
    desc = "Quad 2-input positive-NAND buffers with open collector outputs"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1B", Pin.IN),
        3: Pin("1Y", Pin.OC),
        4: Pin("2A", Pin.IN),
        5: Pin("2B", Pin.IN),
        6: Pin("2Y", Pin.OC),
        8: Pin("3Y", Pin.OC),
        9: Pin("3A", Pin.IN),
        10: Pin("3B", Pin.IN),
        11: Pin("4Y", Pin.OC),
        12: Pin("4A", Pin.IN),
        13: Pin("4B", Pin.IN),
    }