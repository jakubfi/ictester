from binvec import BV
from part import (PackageDIP14, Pin, PinType)
from test import (TestUnivib, UnivibType, UnivibTestType)

class Part74121(PackageDIP14):
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

    tests = [
        TestUnivib("No trigger", UnivibType.UNI_74121, UnivibTestType.NO_TRIGGER),
        TestUnivib("Trigger", UnivibType.UNI_74121, UnivibTestType.TRIGGER),
    ]


