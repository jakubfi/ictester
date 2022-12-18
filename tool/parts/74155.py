from prototypes import (PackageDIP16, Pin, Test)

class Part74155(PackageDIP16):
    name = "74155"
    desc = "Dual 2-line to 4-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("1C", Pin.IN),
        2: Pin("~1G", Pin.IN),
        3: Pin("B", Pin.IN),
        4: Pin("1Y3", Pin.OUT),
        5: Pin("1Y2", Pin.OUT),
        6: Pin("1Y1", Pin.OUT),
        7: Pin("1Y0", Pin.OUT),
        9: Pin("2Y0", Pin.OUT),
        10: Pin("2Y1", Pin.OUT),
        11: Pin("2Y2", Pin.OUT),
        12: Pin("2Y3", Pin.OUT),
        13: Pin("A", Pin.IN),
        14: Pin("~2G", Pin.IN),
        15: Pin("~2C", Pin.IN),
    }
    default_inputs = [3, 13,  2, 1,  14, 15]
    default_outputs = [7, 8, 5, 4,  9, 10, 11, 12]
    test_inhibit = Test("Inhibit", Test.COMB, default_inputs, default_outputs,
        body=[
            [addr + [1, data, 1, data], 8*[1]]
            for addr in Test.binary_combinator(2)
            for data in [0, 1]
        ]
    )
    test_select_0 = Test("Select 0", Test.COMB, default_inputs, default_outputs,
        body=[
            [Test.bin2vec(addr, 2) + [0, 0,  0, 0], [1, 1, 1, 1] + Test.bin2vec(~(1<<(3-addr)), 4)]
            for addr in range(0, 4)
        ]
    )
    test_select_1 = Test("Select 1", Test.COMB, default_inputs, default_outputs,
        body=[
            [Test.bin2vec(addr, 2) + [0, 1,  0, 1], Test.bin2vec(~(1<<(3-addr)), 4) + [1, 1, 1, 1]]
            for addr in range(0, 4)
        ]
    )
    tests = [test_select_0, test_select_1, test_inhibit]
