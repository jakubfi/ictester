from binvec import BV
from part import (PackageDIP16, Pin, PinType)
from test import TestLogic

class Part7489(PackageDIP16):
    name = "7489"
    desc = "64-bit random-access read/write memory"
    pin_cfg = {
        1: Pin("A0", PinType.IN),
        2: Pin("~ME", PinType.IN),
        3: Pin("~WE", PinType.IN),
        4: Pin("D1", PinType.IN),
        5: Pin("~Q1", PinType.OC),
        6: Pin("D2", PinType.IN),
        7: Pin("~Q2", PinType.OC),
        9: Pin("~Q3", PinType.OC),
        10: Pin("D3", PinType.IN),
        11: Pin("~Q4", PinType.OC),
        12: Pin("D4", PinType.IN),
        13: Pin("A3", PinType.IN),
        14: Pin("A2", PinType.IN),
        15: Pin("A1", PinType.IN),
    }

    # ------------------------------------------------------------------------
    def mem_rw_test_gen():
        # --------------------------------------------------------------------
        def rw_cycle(addr_vec):
            return [
                # write 1s
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 1, 1, 1, 1,  0, 0], [0, 0, 0, 0]],  # WRITE: ou = ~in
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 0, 0, 0, 0,  1, 0], [1, 1, 1, 1]],  # WR INHIBIT (with data inputs swapped): ou = ~in
                # read 1s
                [[*addr_vec, 1, 1, 1, 1,  0, 1], [0, 0, 0, 0]],  # READ: ou = ~mem word
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE ou = 1
                # write 0s
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 0, 0, 0, 0,  0, 0], [1, 1, 1, 1]],  # WRITE: ou = ~in
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 1, 1, 1, 1,  1, 0], [0, 0, 0, 0]],  # WR INHIBIT (with data inputs swapped): ou = ~in
                # read 0s
                [[*addr_vec, 0, 0, 0, 0,  0, 1], [1, 1, 1, 1]],  # READ: ou = ~mem word
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
            ]

        body = []

        for v in BV.range(0, 16):
            body.extend(rw_cycle(v))

        return TestLogic("Complete array",
            read_delay_us=0.6,  # 7489 outputs normally require much stronger pullup than what's available in the tester
            inputs=[1, 15, 14, 13,  4, 6, 10, 12,  2, 3],
            outputs=[5, 7, 9, 11],
            body=body,
            loops=256,
        )

    tests = [mem_rw_test_gen()]
