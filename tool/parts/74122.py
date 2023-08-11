from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74122(PackageDIP14):
    UNI_74122 = 1

    name = "74122"
    desc = "Retriggerable Monostable Monovibrators"
    pin_cfg = {
        1: Pin("A1", PinType.IN),
        2: Pin("A2", PinType.IN),
        3: Pin("B1", PinType.IN),
        4: Pin("B2", PinType.IN),
        5: Pin("~CLR", PinType.IN),
        6: Pin("~Q", PinType.OUT),
        8: Pin("Q", PinType.OUT),
        9: Pin("Rint", PinType.NC),
        10: Pin("NC", PinType.NC),
        11: Pin("Cext", PinType.C),
        12: Pin("NC", PinType.NC),
        13: Pin("Rext/Cext", PinType.RC),
    }

    default_inputs=[1, 2, 3, 4, 5],
    default_outputs=[8, 6],

    tests = [
        Test("No trigger", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74122, 0]),
        Test("Trigger", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74122, 1]),
        Test("Retrigger", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74122, 2]),
        Test("Clear", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74122, 3]),
    ]


