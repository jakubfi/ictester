from prototypes import (PackageDIP16, Pin, Test)

class Part74153(PackageDIP16):
    name = "74153"
    desc = "Dual 4-line to 1-line data selectors/multiplexers"
    pin_cfg = {
        1: Pin("~1G", Pin.IN),
        2: Pin("B", Pin.IN),
        3: Pin("1C3", Pin.IN),
        4: Pin("1C2", Pin.IN),
        5: Pin("1C1", Pin.IN),
        6: Pin("1C0", Pin.IN),
        7: Pin("1Y", Pin.OUT),
        9: Pin("2Y", Pin.OUT),
        10: Pin("2C0", Pin.IN),
        11: Pin("2C1", Pin.IN),
        12: Pin("2C2", Pin.IN),
        13: Pin("2C3", Pin.IN),
        14: Pin("A", Pin.IN),
        15: Pin("~2G", Pin.IN),
    }

    default_inputs = [2, 14,  1,  3, 4, 5, 6,  15,  13, 12, 11, 10]
    default_outputs = [7, 9]

    test_select_0 = Test("Select 0", Test.COMB, default_inputs, default_outputs,
        body=[
            [Test.bin2vec(addr, 2) + 2*([0] + Test.bin2vec(~(1<<addr), 4)), [0, 0]]
            for addr in range(0, 4)
        ]
    )
    test_select_1 = Test("Select 1", Test.COMB, default_inputs, default_outputs,
        body=[
            [Test.bin2vec(addr, 2) + 2*([0] + Test.bin2vec(1<<addr, 4)), [1, 1]]
            for addr in range(0, 4)
        ]
    )
    test_inhibit_0 = Test("Inhibit 0", Test.COMB, default_inputs, default_outputs,
        body=[
            [addr + 2*[1,  0, 0, 0, 0], [0, 0]]
            for addr in Test.binary_combinator(2)
        ]
    )
    test_inhibit_1 = Test("Inhibit 1", Test.COMB, default_inputs, default_outputs,
        body=[
            [addr + 2*[1,  1, 1, 1, 1], [0, 0]]
            for addr in Test.binary_combinator(2)
        ]
    )

    tests = [test_select_0, test_select_1, test_inhibit_0, test_inhibit_1]
