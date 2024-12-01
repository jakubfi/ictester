from ictester.part import (Pin, PinType)
from ictester.parts.part_7442 import Part7442

class Part7445(Part7442):
    name = "7445"
    desc = "BCD-to-decimal decoders/drivers"
    pin_cfg = {
        1: Pin("0", PinType.OC),
        2: Pin("1", PinType.OC),
        3: Pin("2", PinType.OC),
        4: Pin("3", PinType.OC),
        5: Pin("4", PinType.OC),
        6: Pin("5", PinType.OC),
        7: Pin("6", PinType.OC),
        9: Pin("7", PinType.OC),
        10: Pin("8", PinType.OC),
        11: Pin("9", PinType.OC),
        12: Pin("D", PinType.IN),
        13: Pin("C", PinType.IN),
        14: Pin("B", PinType.IN),
        15: Pin("A", PinType.IN),
    }
