from prototypes import (PackageDIP24, Pin, Test)

class Part74154(PackageDIP24):
    name = "74154"
    desc = "4-Line-to-16-Line Decoders/Demultiplexers"
    pin_cfg = {
        1: Pin("O0", Pin.OUT),
        2: Pin("O1", Pin.OUT),
        3: Pin("O2", Pin.OUT),
        4: Pin("O3", Pin.OUT),
        5: Pin("O4", Pin.OUT),
        6: Pin("O5", Pin.OUT),
        7: Pin("O6", Pin.OUT),
        8: Pin("O7", Pin.OUT),
        9: Pin("O8", Pin.OUT),
        10: Pin("O9", Pin.OUT),
        11: Pin("O10", Pin.OUT),
        13: Pin("O11", Pin.OUT),
        14: Pin("O12", Pin.OUT),
        15: Pin("O13", Pin.OUT),
        16: Pin("O14", Pin.OUT),
        17: Pin("O15", Pin.OUT),
        18: Pin("G1", Pin.IN),
        19: Pin("G2", Pin.IN),
        20: Pin("D", Pin.IN),
        21: Pin("C", Pin.IN),
        22: Pin("B", Pin.IN),
        23: Pin("A", Pin.IN),
    }
    default_inputs = [18, 19,  20, 21, 22, 23]
    default_outputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]
    test_inhibit = Test("Inhibit", Test.COMB, default_inputs, default_outputs,
        body=[
            [select + addr, 16*[1]]
            for addr in Test.binary_combinator(4)
            for select in [[0, 1], [1, 0], [1, 1]]
        ]
    )
    test_select = Test("Select", Test.COMB, default_inputs, default_outputs,
        body=[
            [[0, 0] + Test.bin2vec(addr, 4), Test.bin2vec(~(1<<(15-addr)), 16)]
            for addr in range(0, 16)
        ]
    )
    tests = [test_select, test_inhibit]
