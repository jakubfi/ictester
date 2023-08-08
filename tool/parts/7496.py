from prototypes import (PackageDIP16_vcc5, Pin, PinType, Test)

class Part7496(PackageDIP16_vcc5):
    name = "7496"
    desc = "5-bit shift register"
    pin_cfg = {
        1: Pin("CLK", PinType.IN),
        2: Pin("A", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("C", PinType.IN),
        6: Pin("D", PinType.IN),
        7: Pin("E", PinType.IN),
        8: Pin("PRE", PinType.IN),
        9: Pin("SER", PinType.IN),
        10: Pin("QE", PinType.OUT),
        11: Pin("QD", PinType.OUT),
        13: Pin("QC", PinType.OUT),
        14: Pin("QB", PinType.OUT),
        15: Pin("QA", PinType.OUT),
        16: Pin("CLR", PinType.IN),
    }

    default_inputs = [16, 8,  2, 3, 4, 6, 7,  1, 9]
    default_outputs = [15, 14, 13, 11, 10]

    test_preset = Test("Preset", Test.COMB, default_inputs, default_outputs,
        body=[
            # preset all 1
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            # clear
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset selective 1s
            [[1, 1,  0, 0, 0, 0, 1,  0, 0], [0, 0, 0, 0, 1]],
            [[1, 1,  0, 0, 0, 1, 0,  0, 0], [0, 0, 0, 1, 1]],
            [[1, 1,  0, 0, 1, 0, 0,  0, 0], [0, 0, 1, 1, 1]],
            [[1, 1,  0, 1, 0, 0, 0,  0, 0], [0, 1, 1, 1, 1]],
            [[1, 1,  1, 0, 0, 0, 0,  0, 0], [1, 1, 1, 1, 1]],
            # clear, preset known
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            [[1, 1,  0, 1, 0, 1, 0,  0, 0], [0, 1, 0, 1, 0]],
            # no action
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 1, 0, 1, 0]],
        ]
    )
    test_clear = Test("Clear", Test.COMB, default_inputs, default_outputs,
        body=[
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 1,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            # preset/clear
            [[1, 1,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[0, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 0, 0]],
        ]
    )
    test_serial_in = Test("Serial in", Test.COMB, default_inputs, default_outputs,
        body=[
            # clear, preset known
            [[0, 0,  0, 0, 0, 0, 0,  0, 0], [0, 0, 0, 0, 0]],
            [[1, 1,  1, 0, 1, 0, 1,  0, 0], [1, 0, 1, 0, 1]],
            # shift in 1s
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 0, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 0, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 0, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 1, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 1], [1, 1, 1, 1, 0]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1, 1]],
            # shift in 0s
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 1, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 1, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 1, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  0, 0], [0, 0, 0, 0, 1]],
            [[1, 0,  1, 1, 1, 1, 1,  1, 0], [0, 0, 0, 0, 0]],
        ]
    )

    tests = [test_preset, test_clear, test_serial_in]
