from prototypes import (Pin, partimport)

class Part7445(partimport("7442")):
    name = "7445"
    desc = "BCD-to-decimal decoders/drivers"
    pin_cfg = {
        1: Pin("0", Pin.OC),
        2: Pin("1", Pin.OC),
        3: Pin("2", Pin.OC),
        4: Pin("3", Pin.OC),
        5: Pin("4", Pin.OC),
        6: Pin("5", Pin.OC),
        7: Pin("6", Pin.OC),
        9: Pin("7", Pin.OC),
        10: Pin("8", Pin.OC),
        11: Pin("9", Pin.OC),
        12: Pin("D", Pin.IN),
        13: Pin("C", Pin.IN),
        14: Pin("B", Pin.IN),
        15: Pin("A", Pin.IN),
    }