# ------------------------------------------------------------------------
class Pin:
    INPUT = 1
    OUTPUT = 2
    OC = 3
    POWER = 4
    NC = 5

    def __init__(self, pin, name, role):
        self.pin = pin
        self.name = name
        self.role = role

# ------------------------------------------------------------------------
class Part:
    pincount = 0
    name = None
    package_name = None

    def vector_by_pins(self, vector):
        """
        translate given test vector [[inputs], [outputs]] in user order
        to a test vector [i/o] in pin order
        """
        v_positions = self.vector_in + self.vector_out
        v = vector[0] + vector[1]
        v_out = []
        for p in self.pins:
            if p.role in [Pin.INPUT, Pin.OUTPUT, Pin.OC]:
                val = v[v_positions.index(p.pin)]
                v_out.append(val)
            else:
                v_out.append(0)
        return v_out

# ------------------------------------------------------------------------
class PartDIP14(Part):
    package_name = "DIP14"
    pincount = 14

# ------------------------------------------------------------------------
class PartDIP16(Part):
    package_name = "DIP16"
    pincount = 16

# ------------------------------------------------------------------------
class PartDIP24(Part):
    package_name = "DIP24"
    pincount = 24

