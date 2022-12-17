from prototypes import Pin
Part7410 = __import__('parts.7410', fromlist=['Part7410']).Part7410

class Part7412(Part7410):
    name = "7412"
    desc = "Triple 3-input positive-NAND gates with open-collector outputs"
    pin_cfg = {
        1: Pin("1A", Pin.IN),
        2: Pin("1B", Pin.IN),
        3: Pin("2A", Pin.IN),
        4: Pin("2B", Pin.IN),
        5: Pin("2C", Pin.IN),
        6: Pin("2Y", Pin.OC),
        8: Pin("3Y", Pin.OC),
        9: Pin("3A", Pin.IN),
        10: Pin("3B", Pin.IN),
        11: Pin("3C", Pin.IN),
        12: Pin("1Y", Pin.OC),
        13: Pin("1C", Pin.IN),
    }