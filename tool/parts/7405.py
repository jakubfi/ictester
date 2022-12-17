from prototypes import Pin
Part7404 = __import__('parts.7404', fromlist=['Part7404']).Part7404

class Part7405(Part7404):
    name = "7405"
    desc = "Hex inverters with open collector outputs"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1Y", Pin.OC),
        3: Pin("2A", Pin.IN),
        4: Pin("2Y", Pin.OC),
        5: Pin("3A", Pin.IN),
        6: Pin("3Y", Pin.OC),
        8: Pin("6Y", Pin.OC),
        9: Pin("6A", Pin.IN),
        10: Pin("5Y", Pin.OC),
        11: Pin("5A", Pin.IN),
        12: Pin("4Y", Pin.OC),
        13: Pin("4A", Pin.IN),
    }
