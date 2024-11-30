from part import (Pin, PinType)
from parts.part_7410 import Part7410

class Part7412(Part7410):
    name = "7412"
    desc = "Triple 3-input positive-NAND gates with open-collector outputs"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("2A", PinType.IN),
        4: Pin("2B", PinType.IN),
        5: Pin("2C", PinType.IN),
        6: Pin("2Y", PinType.OC),
        8: Pin("3Y", PinType.OC),
        9: Pin("3A", PinType.IN),
        10: Pin("3B", PinType.IN),
        11: Pin("3C", PinType.IN),
        12: Pin("1Y", PinType.OC),
        13: Pin("1C", PinType.IN),
    }
