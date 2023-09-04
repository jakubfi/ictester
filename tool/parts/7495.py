from prototypes import (PackageDIP14, Pin, PinType, Test)

class Part7495(PackageDIP14):
    name = "7495"
    desc = "4-bit parallel-access shift registers"
    pin_cfg = {
        1: Pin("SER", PinType.IN),
        2: Pin("A", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("C", PinType.IN),
        5: Pin("D", PinType.IN),
        6: Pin("MODE", PinType.IN),
        8: Pin("CLK2", PinType.IN),
        9: Pin("CLK1", PinType.IN),
        10: Pin("QD", PinType.OUT),
        11: Pin("QC", PinType.OUT),
        12: Pin("QB", PinType.OUT),
        13: Pin("QA", PinType.OUT),
    }

    default_inputs = [6, 8, 9, 1, 2, 3, 4, 5]
    default_outputs = [13, 12, 11, 10]

    test_load = Test("Parallel load", Test.LOGIC, default_inputs, default_outputs,
        body=[
            [[1, '\\', 0, 0, 1, 1, 1, 1], [1, 1, 1, 1]],
            [[1, '\\', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )
    test_rshift = Test("Right Shift", Test.LOGIC, default_inputs, default_outputs,
        body=[
            # set known starting value
            [[1, '\\', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            # test shift
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, '\\', 1, 0, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 1, 0, 0]],
            [[0, 0, '\\', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '\\', 1, 0, 0, 0, 0], [1, 0, 1, 0]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 1, 0, 1]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 0, 1, 0]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 0, 0, 1]],
            [[0, 0, '\\', 0, 0, 0, 0, 0], [0, 0, 0, 0]],
        ]
    )

    tests = [test_load, test_rshift]
