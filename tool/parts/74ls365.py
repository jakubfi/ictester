from binvec import BV
from prototypes import (PackageDIP16, Pin, PinType, TestLogic)

class Part7404(PackageDIP16):
    name = "74LS365"
    desc = "3-state Hex Buffers"
    pin_cfg = {
        1: Pin("~E1", PinType.IN),
        2: Pin("1A", PinType.IN),
        3: Pin("1Y", PinType.ST3),
        4: Pin("2A", PinType.IN),
        5: Pin("2Y", PinType.ST3),
        6: Pin("3A", PinType.IN),
        7: Pin("3Y", PinType.ST3),
        9: Pin("6Y", PinType.ST3),
        10: Pin("6A", PinType.IN),
        11: Pin("5Y", PinType.ST3),
        12: Pin("5A", PinType.IN),
        13: Pin("4Y", PinType.ST3),
        14: Pin("4A", PinType.IN),
        15: Pin("~E2", PinType.IN),
    }

    tests = [
        TestLogic("Outputs enabled",
            inputs=[1, 15,  2, 4, 6, 14, 12, 10],
            outputs=[3, 5, 7, 13, 11, 9],
            body=[
                [[0, 0, *(6*x)], 6*x]
                for x in BV.range(0, 2)
            ]
        ),
        TestLogic("Outputs disabled",
            read_delay_us=2.6,  # with weak pullup, disabled (HiZ) outputs require more time to settle
            inputs=[1, 15,  2, 4, 6, 14, 12, 10],
            outputs=[3, 5, 7, 13, 11, 9],
            body=[
                [[*e, *(6*x)], 6*[1]]
                for x in BV.range(0, 2)
                for e in [[1, 1], [0, 1], [1, 0]]
            ]
        )
    ]
