from prototypes import (PackageDIP16, Pin, Test)

class Part7489(PackageDIP16):
    name = "7489"
    desc = "64-bit random-access read/write memory"
    pin_cfg = {
        1: Pin("A0", Pin.IN),
        2: Pin("~ME", Pin.IN),
        3: Pin("~WE", Pin.IN),
        4: Pin("D1", Pin.IN),
        5: Pin("~Q1", Pin.OC),
        6: Pin("D2", Pin.IN),
        7: Pin("~Q2", Pin.OC),
        9: Pin("~Q3", Pin.OC),
        10: Pin("D3", Pin.IN),
        11: Pin("~Q4", Pin.OC),
        12: Pin("D4", Pin.IN),
        13: Pin("A3", Pin.IN),
        14: Pin("A2", Pin.IN),
        15: Pin("A1", Pin.IN),
    }
    # ------------------------------------------------------------------------
    def mem_rw_test_gen():
        # --------------------------------------------------------------------
        def rw_cycle(addr_vec):
            return [
                # write 1s
                [addr_vec + [1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [addr_vec + [1, 1, 1, 1,  0, 0], [0, 0, 0, 0]],  # WRITE: ou = ~in
                [addr_vec + [1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [addr_vec + [0, 0, 0, 0,  1, 0], [1, 1, 1, 1]],  # WR INHIBIT (with data inputs swapped): ou = ~in
                # read 1s
                [addr_vec + [1, 1, 1, 1,  0, 1], [0, 0, 0, 0]],  # READ: ou = ~mem word
                [addr_vec + [1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE ou = 1
                # write 0s
                [addr_vec + [0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [addr_vec + [0, 0, 0, 0,  0, 0], [1, 1, 1, 1]],  # WRITE: ou = ~in
                [addr_vec + [0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [addr_vec + [1, 1, 1, 1,  1, 0], [0, 0, 0, 0]],  # WR INHIBIT (with data inputs swapped): ou = ~in
                # read 0s
                [addr_vec + [0, 0, 0, 0,  0, 1], [1, 1, 1, 1]],  # READ: ou = ~mem word
                [addr_vec + [0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
            ]

        body = []
        for v in Test.binary_combinator(4):
            body.extend(rw_cycle(v))

        return Test(
            name="Complete array",
            inputs=[1, 15, 14, 13,  4, 6, 10, 12,  2, 3],
            outputs=[5, 7, 9, 11],
            ttype=Test.COMB,
            body=body,
            loops=256,
        )

    tests = [mem_rw_test_gen()]