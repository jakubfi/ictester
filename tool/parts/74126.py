from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part74126(PackageDIP14):
    name = "74126"
    desc = "Quarduple bus buffers with 3-state outputs"
    pin_cfg = {
        1: Pin("1G", PinType.IN),
        2: Pin("1A", PinType.IN),
        3: Pin("1Y", PinType.OC),
        4: Pin("2G", PinType.IN),
        5: Pin("2A", PinType.IN),
        6: Pin("2Y", PinType.OC),
        8: Pin("3Y", PinType.OC),
        9: Pin("3A", PinType.IN),
        10: Pin("3G", PinType.IN),
        11: Pin("4Y", PinType.OC),
        12: Pin("4A", PinType.IN),
        13: Pin("4G", PinType.IN),
    }

    test_all = Test("Complete logic", Test.LOGIC,
        inputs=[1, 2,  4, 5,  10, 9,  13, 12],
        outputs=[3, 6, 8, 11],
        body=[
            [[1, 1,  1, 1,  1, 1,  1, 1], [1, 1, 1, 1]],
            [[1, 0,  1, 0,  1, 0,  1, 0], [0, 0, 0, 0]],
            [[0, 1,  0, 1,  0, 1,  0, 1], [1, 1, 1, 1]],
            [[0, 0,  0, 0,  0, 0,  0, 0], [1, 1, 1, 1]],
        ]
    )

    tests = [test_all]
