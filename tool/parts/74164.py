from prototypes import (PackageDIP14, Pin, PinType, TestLogic)

class Part74164(PackageDIP14):
    name = "74164"
    desc = "8-bit parallel-out serial shift register"
    pin_cfg = {
        1: Pin("A", PinType.IN),
        2: Pin("B", PinType.IN),
        3: Pin("QA", PinType.IN),
        4: Pin("QB", PinType.IN),
        5: Pin("QC", PinType.IN),
        6: Pin("QD", PinType.IN),
        8: Pin("CLK", PinType.IN),
        9: Pin("~CLR", PinType.IN),
        10: Pin("QE", PinType.IN),
        11: Pin("QF", PinType.OUT),
        12: Pin("QG", PinType.OUT),
        13: Pin("QH", PinType.OUT),
    }

    test_all = TestLogic("Complete logic",
        inputs=[9, 8,  1, 2],
        outputs=[3, 4, 5, 6, 10, 11, 12, 13],
        body=[
            # clear
            [[0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            # idle
            [[1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            [[1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]],
            # shift in
            [[1, '/', 1, 1], [1, 0, 0, 0, 0, 0, 0, 0]],
            [[1, '/', 0, 1], [0, 1, 0, 0, 0, 0, 0, 0]],
            [[1, '/', 1, 0], [0, 0, 1, 0, 0, 0, 0, 0]],
            [[1, '/', 0, 0], [0, 0, 0, 1, 0, 0, 0, 0]],
            [[1, '/', 1, 1], [1, 0, 0, 0, 1, 0, 0, 0]],
            [[1, '/', 1, 1], [1, 1, 0, 0, 0, 1, 0, 0]],
            [[1, '/', 1, 1], [1, 1, 1, 0, 0, 0, 1, 0]],
            [[1, '/', 1, 1], [1, 1, 1, 1, 0, 0, 0, 1]],
            [[1, '/', 1, 1], [1, 1, 1, 1, 1, 0, 0, 0]],
            [[1, '/', 1, 1], [1, 1, 1, 1, 1, 1, 0, 0]],
            [[1, '/', 1, 1], [1, 1, 1, 1, 1, 1, 1, 0]],
            [[1, '/', 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
            # clear
            [[0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        ]
    )

    tests = [test_all]
