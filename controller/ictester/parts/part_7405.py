from ictester.part import (Pin, PinType)
from ictester.parts.part_7404 import Part7404

class Part7405(Part7404):
    name = "7405"
    desc = "Hex inverters with open collector outputs"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1Y", PinType.OC),
        3: Pin("2A", PinType.IN),
        4: Pin("2Y", PinType.OC),
        5: Pin("3A", PinType.IN),
        6: Pin("3Y", PinType.OC),
        8: Pin("6Y", PinType.OC),
        9: Pin("6A", PinType.IN),
        10: Pin("5Y", PinType.OC),
        11: Pin("5A", PinType.IN),
        12: Pin("4Y", PinType.OC),
        13: Pin("4A", PinType.IN),
    }
