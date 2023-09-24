from binvec import BV
from part import partimport
from test import TestLogic

class Part780101(partimport("7489")):
    name = "780101"
    '''
    Similar to 7489. Same pinout, but differences in behavior:
     * outputs are always high during write
     * outputs are always high when CS is high
    '''

    # ------------------------------------------------------------------------
    def mem_rw_test_gen():
        # --------------------------------------------------------------------
        def rw_cycle(addr_vec):
            return [
                # write 1s
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 1, 1, 1, 1,  0, 0], [1, 1, 1, 1]],  # WRITE: ou = 1
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 0, 0, 0, 0,  1, 0], [1, 1, 1, 1]],  # NONE: ou = 1
                # read 1s
                [[*addr_vec, 1, 1, 1, 1,  0, 1], [0, 0, 0, 0]],  # READ: ou = ~mem word
                [[*addr_vec, 1, 1, 1, 1,  1, 1], [1, 1, 1, 1]],  # NONE ou = 1
                # write 0s
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 0, 0, 0, 0,  0, 0], [1, 1, 1, 1]],  # WRITE: ou = 1
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
                [[*addr_vec, 1, 1, 1, 1,  1, 0], [1, 1, 1, 1]],  # NONE: ou = 1
                # read 0s
                [[*addr_vec, 0, 0, 0, 0,  0, 1], [1, 1, 1, 1]],  # READ: ou = ~mem word
                [[*addr_vec, 0, 0, 0, 0,  1, 1], [1, 1, 1, 1]],  # NONE: ou = 1
            ]

        body = []

        for v in BV.range(0, 16):
            body.extend(rw_cycle(v))

        return TestLogic("Complete array",
            read_delay_us=0.6,  # 780101 outputs normally require much stronger pullup than what's available in the tester
            inputs=[1, 15, 14, 13,  4, 6, 10, 12,  2, 3],
            outputs=[5, 7, 9, 11],
            body=body,
            loops=256,
        )

    tests = [mem_rw_test_gen()]
