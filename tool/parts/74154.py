from binvec import BV
from prototypes import (PackageDIP24, Pin, PinType, Test)

class Part74154(PackageDIP24):
    name = "74154"
    desc = "4-Line-to-16-Line Decoders/Demultiplexers"
    pin_cfg = {
        1: Pin("O0", PinType.OUT),
        2: Pin("O1", PinType.OUT),
        3: Pin("O2", PinType.OUT),
        4: Pin("O3", PinType.OUT),
        5: Pin("O4", PinType.OUT),
        6: Pin("O5", PinType.OUT),
        7: Pin("O6", PinType.OUT),
        8: Pin("O7", PinType.OUT),
        9: Pin("O8", PinType.OUT),
        10: Pin("O9", PinType.OUT),
        11: Pin("O10", PinType.OUT),
        13: Pin("O11", PinType.OUT),
        14: Pin("O12", PinType.OUT),
        15: Pin("O13", PinType.OUT),
        16: Pin("O14", PinType.OUT),
        17: Pin("O15", PinType.OUT),
        18: Pin("G1", PinType.IN),
        19: Pin("G2", PinType.IN),
        20: Pin("D", PinType.IN),
        21: Pin("C", PinType.IN),
        22: Pin("B", PinType.IN),
        23: Pin("A", PinType.IN),
    }

    default_inputs = [18, 19,  20, 21, 22, 23]
    default_outputs = [17, 16, 15, 14, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    test_inhibit = Test("Inhibit", Test.COMB, default_inputs, default_outputs,
        body=[
            [[*select, *addr],  ~BV.int(0, 16)]
            for addr in BV.range(0, 16)
            for select in [[0, 1], [1, 0], [1, 1]]
        ]
    )
    test_select = Test("Select", Test.COMB, default_inputs, default_outputs,
        body=[[[0, 0, *BV.int(addr, 4)],  [*~BV.bit(addr, 16)]] for addr in range(0, 16)]
    )

    tests = [test_select, test_inhibit]
