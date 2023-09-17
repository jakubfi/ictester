from binvec import BV
from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part74LS51(PackageDIP14):
    name = "74LS51"
    desc = "Invert Gates"
    pin_cfg = {
        1: Pin("1A", PinType.IN),
        2: Pin("2A", PinType.IN),
        3: Pin("2B", PinType.IN),
        4: Pin("2C", PinType.IN),
        5: Pin("2D", PinType.IN),
        6: Pin("2Y", PinType.OUT),
        8: Pin("1Y", PinType.OUT),
        9: Pin("1D", PinType.IN),
        10: Pin("1E", PinType.IN),
        11: Pin("1F", PinType.IN),
        12: Pin("1B", PinType.IN),
        13: Pin("1C", PinType.IN),
    }

    test_gate1 = TestLogic("Gate 1",
        inputs=[1, 12, 13,  9, 10, 11],
        outputs=[8],
        body=[
            [[*abc, *_def],  [not (abc.vand() or _def.vand())]]
            for abc in BV.range(0, 8)
            for _def in BV.range(0, 8)
        ]
    )

    test_gate2 = TestLogic("Gate 2",
        inputs=[2, 3,  4, 5],
        outputs=[6],
        body=[
            [[*ab, *cd],  [not (ab.vand() or cd.vand())]]
            for ab in BV.range(0, 4)
            for cd in BV.range(0, 4)
        ]
    )


    tests = [test_gate1, test_gate2]
