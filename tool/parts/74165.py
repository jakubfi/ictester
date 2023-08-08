#from prototypes import (PackageDIP16, Pin, PinType, Test)
#
#class Part74165(PackageDIP16):
#    name = "74165"
#    desc = "8-bit parallel-out serial shift register"
#    pin_cfg = {
#        1: Pin("SH/~LD", PinType.IN),
#        2: Pin("CLK", PinType.IN),
#        3: Pin("E", PinType.IN),
#        4: Pin("F", PinType.IN),
#        5: Pin("G", PinType.IN),
#        6: Pin("H", PinType.IN),
#        7: Pin("~QH", PinType.OUT),
#        9: Pin("QH", PinType.OUT),
#        10: Pin("SER", PinType.IN),
#        11: Pin("A", PinType.IN),
#        12: Pin("B", PinType.IN),
#        13: Pin("C", PinType.IN),
#        14: Pin("D", PinType.IN),
#        15: Pin("CLK INH", PinType.IN),
#    }
#    test_all = Test(
#        name="Complete logic",
#        inputs=[1, 15, 2,  10,  11, 12, 13, 14, 3, 4, 5, 6],
#        outputs=[9, 7],
#        ttype=Test.SEQ,
#        body=[
#            [['-', 0,   0,  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [0, 1]],
#
#            [['-', 0,   0,  0,  1, 1, 1, 1, 1, 1, 1, 1], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 1]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#            [[  1, 0, '+',  0,  0, 0, 0, 0, 0, 0, 0, 0], [1, 0]],
#        ]
#    )
#    tests = [test_all]
