from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, TestUnivib)

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
        TestUnivib("No trigger", UNI_74121, 0, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Trigger", UNI_74121, 1, inputs=default_inputs, outputs=default_outputs),
    ]


