from prototypes import Pin
Part74155 = __import__('parts.74155', fromlist=['Part74155']).Part74155

class Part74156(Part74155):
    name = "74156"
    desc = "Dual 2-line to 4-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("1C", Pin.IN),
        2: Pin("~1G", Pin.IN),
        3: Pin("B", Pin.IN),
        4: Pin("1Y3", Pin.OC),
        5: Pin("1Y2", Pin.OC),
        6: Pin("1Y1", Pin.OC),
        7: Pin("1Y0", Pin.OC),
        9: Pin("2Y0", Pin.OC),
        10: Pin("2Y1", Pin.OC),
        11: Pin("2Y2", Pin.OC),
        12: Pin("2Y3", Pin.OC),
        13: Pin("A", Pin.IN),
        14: Pin("~2G", Pin.IN),
        15: Pin("~2C", Pin.IN),
    }
