from prototypes import (PackageDIP16, Pin, Test)

class Part74S201(PackageDIP16):
    name = "74S201"
    desc = "256-bit high-performance random-access memory"
    pin_cfg = {
        1: Pin("A0", Pin.IN),
        2: Pin("A1", Pin.IN),
        3: Pin("~S1", Pin.IN),
        4: Pin("~S2", Pin.IN),
        5: Pin("~S3", Pin.IN),
        6: Pin("~Q", Pin.OC),
        7: Pin("A3", Pin.IN),
        9: Pin("A4", Pin.IN),
        10: Pin("A5", Pin.IN),
        11: Pin("A6", Pin.IN),
        12: Pin("R/~W", Pin.IN),
        13: Pin("D", Pin.IN),
        14: Pin("A7", Pin.IN),
        15: Pin("A2", Pin.IN),
    }

    # ------------------------------------------------------------------------
    def for_all_addr(op, s1, s2, s3, i, o):
        return [
            [[op,  s1, s2, s3] + Test.bin2vec(addr, 8) + [i], [o]]
            for addr in range(0, 256)
        ]

    test_rw = Test(
        name="R/W all address space",
        inputs=[12,  3, 4, 5,  1, 2, 15, 7, 9, 10, 11, 14,  13],
        outputs=[6],
        ttype=Test.COMB,
        loops=32,
        body= for_all_addr(0,  0, 0, 0,  0,  1)  # write '0', output = high impedance
            + for_all_addr(1,  0, 0, 0,  0,  1)  # read, output = '1'
            + for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + for_all_addr(1,  0, 0, 0,  0,  0)  # read, output = '0'
    )
    test_inhibit_read = Test(
        name="Inhibit read",
        inputs=[12,  3, 4, 5,  1, 2, 15, 7, 9, 10, 11, 14,  13],
        outputs=[6],
        ttype=Test.COMB,
        loops=32,
        body= for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + for_all_addr(1,  0, 0, 1,  0,  1)  # inhibit read, output = high impedance
            + for_all_addr(1,  0, 1, 0,  0,  1)  # inhibit read, output = high impedance
            + for_all_addr(1,  1, 0, 0,  0,  1)  # inhibit read, output = high impedance
    )
    test_inhibit_write = Test(
        name="Inhibit write",
        inputs=[12,  3, 4, 5,  1, 2, 15, 7, 9, 10, 11, 14,  13],
        outputs=[6],
        ttype=Test.COMB,
        loops=32,
        body= for_all_addr(0,  0, 0, 0,  1,  1)  # write '1', output = high impedance
            + [[[1, 1, 1, 1,  0, 0, 0, 0, 0, 0, 0, 0,  0], [1]]]  # set inhibit
            + for_all_addr(0,  1, 1, 1,  0,  1)  # inhibit write '1', output = high impedance
            + for_all_addr(1,  0, 0, 0,  0,  0)  # inhibit read, output = 0
    )

    tests = [test_rw, test_inhibit_read, test_inhibit_write]
