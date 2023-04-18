from prototypes import (PackageDIP16, Pin, Test)

class Part7485(PackageDIP16):
    name = "7485"
    desc = "4-bit magnitude comparator"
    pin_cfg = {
        1: Pin("B3", Pin.IN),
        2: Pin("A<Bin", Pin.IN),
        3: Pin("A=Bin", Pin.IN),
        4: Pin("A>Bin", Pin.IN),
        5: Pin("A>Bout", Pin.OUT),
        6: Pin("A=Bout", Pin.OUT),
        7: Pin("A<Bout", Pin.OUT),
        9: Pin("B0", Pin.IN),
        10: Pin("A0", Pin.IN),
        11: Pin("B1", Pin.IN),
        12: Pin("A1", Pin.IN),
        13: Pin("A2", Pin.IN),
        14: Pin("B2", Pin.IN),
        15: Pin("A3", Pin.IN),
    }

    test_all = Test("Full logic", Test.COMB,
        inputs=[2, 3, 4,  15, 13, 12, 10,  1, 14, 11, 9],
        outputs=[7, 6, 5],
        loops=256,
        body=[
            [[ls, eq, gt] + Test.bin2vec(a, 4) + Test.bin2vec(b, 4), [
                (a < b) or ((a == b) and (ls or not any([ls, eq, gt]))),
                (a == b) and eq,
                (a > b) or ((a == b) and (gt or not any([ls, eq, gt])))
            ]]
            for a in range(16)
            for b in range(16)
            for ls in range(1)
            for eq in range(1)
            for gt in range(1)
        ]
    )

    tests = [test_all]
