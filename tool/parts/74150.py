from prototypes import (PackageDIP24, Pin, Test)

class Part74150(PackageDIP24):
    name = "74150"
    desc = "Data selectors/multiplexers"
    pin_cfg = {
        1: Pin("E7", Pin.IN),
        2: Pin("E6", Pin.IN),
        3: Pin("E5", Pin.IN),
        4: Pin("E4", Pin.IN),
        5: Pin("E3", Pin.IN),
        6: Pin("E2", Pin.IN),
        7: Pin("E1", Pin.IN),
        8: Pin("E0", Pin.IN),
        9: Pin("~G", Pin.IN),
        10: Pin("W", Pin.OUT),
        11: Pin("D", Pin.IN),
        13: Pin("C", Pin.IN),
        14: Pin("B", Pin.IN),
        15: Pin("A", Pin.IN),
        16: Pin("E15", Pin.IN),
        17: Pin("E14", Pin.IN),
        18: Pin("E13", Pin.IN),
        19: Pin("E12", Pin.IN),
        20: Pin("E11", Pin.IN),
        21: Pin("E10", Pin.IN),
        22: Pin("E9", Pin.IN),
        23: Pin("E8", Pin.IN),
    }
    default_inputs = [11, 13, 14, 15,  9,  8, 7, 6, 5, 4, 3, 2, 1, 23, 22, 21, 20, 19, 18, 17, 16]
    default_outputs = [10]
    test_select_0 = Test("Select 0", Test.COMB,
        inputs=default_inputs, outputs=default_outputs,
        body=[
            [Test.bin2vec(addr, 4) + [0] + Test.bin2vec(~(1<<(15-addr)), 16), [1]]
            for addr in range(0, 15)
        ]
    )
    test_select_1 = Test("Select 1", Test.COMB, default_inputs, default_outputs,
        body=[
            [Test.bin2vec(addr, 4) + [0] + Test.bin2vec((1<<(15-addr)), 16), [0]]
            for addr in range(0, 15)
        ]
    )
    test_inhibit_0 = Test("Inhibit 0", Test.COMB, default_inputs, default_outputs,
        body=[
            [addr + [1] + 16*[0], [1]]
            for addr in Test.binary_combinator(4)
        ]
    )
    test_inhibit_1 = Test("Inhibit 1", Test.COMB, default_inputs, default_outputs,
        body=[
            [addr + [1] + 16*[1], [1]]
            for addr in Test.binary_combinator(4)
        ]
    )
    tests = [test_select_0, test_select_1, test_inhibit_0, test_inhibit_1]