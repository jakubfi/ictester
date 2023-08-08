from prototypes import (Pin, PinType, partimport)

class Part74156(partimport("74155")):
    name = "74156"
    desc = "Dual 2-line to 4-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("1C", PinType.IN),
        2: Pin("~1G", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("1Y3", PinType.OC),
        5: Pin("1Y2", PinType.OC),
        6: Pin("1Y1", PinType.OC),
        7: Pin("1Y0", PinType.OC),
        9: Pin("2Y0", PinType.OC),
        10: Pin("2Y1", PinType.OC),
        11: Pin("2Y2", PinType.OC),
        12: Pin("2Y3", PinType.OC),
        13: Pin("A", PinType.IN),
        14: Pin("~2G", PinType.IN),
        15: Pin("~2C", PinType.IN),
    }
