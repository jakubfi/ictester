from binvec import BV
from prototypes import (PackageDIP16, Pin, PinType, TestUnivib, UnivibType, UnivibTestType)

class Part74123(PackageDIP16):
    name = "74123"
    desc = "Dual Retriggerable Monostable Monovibrators"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("1B", PinType.IN),
        3: Pin("~1CLR", PinType.IN),
        4: Pin("~1Q", PinType.OUT),
        5: Pin("2Q", PinType.OUT),
        6: Pin("2Cext", PinType.C),
        7: Pin("2Rext/Cext", PinType.RC),
        9: Pin("2A", PinType.IN),
        10: Pin("2B", PinType.IN),
        11: Pin("~2CLR", PinType.IN),
        12: Pin("~2Q", PinType.OUT),
        13: Pin("1Q", PinType.OUT),
        14: Pin("1Cext", PinType.C),
        15: Pin("1Rext/Cext", PinType.RC),
    }

    tests = [
        TestUnivib("Univibrator 1, no trigger", UnivibType.UNI_74123_1, UnivibTestType.NO_TRIGGER),
        TestUnivib("Univibrator 1, trigger", UnivibType.UNI_74123_1, UnivibTestType.TRIGGER),
        TestUnivib("Univibrator 1, retrigger", UnivibType.UNI_74123_1, UnivibTestType.RETRIGGER),
        TestUnivib("Univibrator 1, clear-trigger", UnivibType.UNI_74123_1, UnivibTestType.CLEAR_TRIGGER),
        TestUnivib("Univibrator 1, clear", UnivibType.UNI_74123_1, UnivibTestType.CLEAR),
        TestUnivib("Univibrator 1, no cross-trigger", UnivibType.UNI_74123_1, UnivibTestType.NO_CROSS_TRIGGER),
        TestUnivib("Univibrator 2, no trigger", UnivibType.UNI_74123_2, UnivibTestType.NO_TRIGGER),
        TestUnivib("Univibrator 2, trigger", UnivibType.UNI_74123_2, UnivibTestType.TRIGGER),
        TestUnivib("Univibrator 2, retrigger", UnivibType.UNI_74123_2, UnivibTestType.RETRIGGER),
        TestUnivib("Univibrator 2, clear-trigger", UnivibType.UNI_74123_2, UnivibTestType.CLEAR_TRIGGER),
        TestUnivib("Univibrator 2, clear", UnivibType.UNI_74123_2, UnivibTestType.CLEAR),
        TestUnivib("Univibrator 2, no cross-trigger", UnivibType.UNI_74123_2, UnivibTestType.NO_CROSS_TRIGGER),
    ]


