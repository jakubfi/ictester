from ictester.binvec import BV
from ictester.part import (PackageDIP14, Pin, PinType)
from ictester.test import (TestUnivib, UnivibType, UnivibTestType)

class Part74122(PackageDIP14):
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

    tests = [
        TestUnivib("No trigger", UnivibType.UNI_74122, UnivibTestType.NO_TRIGGER),
        TestUnivib("Trigger", UnivibType.UNI_74122, UnivibTestType.TRIGGER),
        TestUnivib("Retrigger", UnivibType.UNI_74122, UnivibTestType.RETRIGGER),
        TestUnivib("Clear", UnivibType.UNI_74122, UnivibTestType.CLEAR),
    ]


