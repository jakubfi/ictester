from binvec import BV
from prototypes import (PackageDIP16, Pin, PinType, TestUnivib)

class Part74123(PackageDIP16):
    UNI_74123_1 = 2
    UNI_74123_2 = 3

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

    default_inputs=[1, 2, 3,  9, 10, 11],
    default_outputs=[13, 4,  5, 12],
    tests = [
        TestUnivib("Univibrator 1, no trigger", UNI_74123_1, 0, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 1, trigger", UNI_74123_1, 1, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 1, retrigger", UNI_74123_1, 2, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 1, clear-trigger", UNI_74123_1, 5, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 1, clear", UNI_74123_1, 3, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 1, no cross-trigger", UNI_74123_1, 4, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, no trigger", UNI_74123_2, 0, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, trigger", UNI_74123_2, 1, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, retrigger", UNI_74123_2, 2, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, clear-trigger", UNI_74123_2, 5, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, clear", UNI_74123_2, 3, inputs=default_inputs, outputs=default_outputs),
        TestUnivib("Univibrator 2, no cross-trigger", UNI_74123_2, 4, inputs=default_inputs, outputs=default_outputs),
    ]


