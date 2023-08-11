from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74121(PackageDIP14):
    UNI_74121 = 0

    name = "74121"
    desc = "Monostable Monovibrators With Schmitt-trigger Inputs"
    pin_cfg = {
        1: Pin("~Q", PinType.OUT),
        2: Pin("NC", PinType.NC),
        3: Pin("A1", PinType.IN),
        4: Pin("A2", PinType.IN),
        5: Pin("B", PinType.IN),
        6: Pin("Q", PinType.OUT),
        8: Pin("NC", PinType.NC),
        9: Pin("Rint", PinType.NC),
        10: Pin("Cext", PinType.C),
        11: Pin("Rext/Cext", PinType.RC),
        12: Pin("NC", PinType.NC),
        13: Pin("NC", PinType.NC),
    }

    default_inputs=[3, 4, 5]
    default_outputs=[6, 1]

    tests = [
        Test("No trigger", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74121, 0]),
        Test("Trigger", Test.UNIVIB, default_inputs, default_outputs, params=[UNI_74121, 1]),
    ]


