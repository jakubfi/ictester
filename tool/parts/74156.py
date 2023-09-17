from prototypes import (Pin, PinType, PackageDIP16, TestLogic)
from binvec import BV

class Part74156(PackageDIP16):
    name = "74156"
    desc = "Dual 2-line to 4-line decoders/demultiplexers"
    pin_cfg = {
        1: Pin("1C", PinType.IN),
        2: Pin("~1G", PinType.IN),
        3: Pin("B", PinType.IN),
        4: Pin("1Y3", PinType.OC),
        5: Pin("1Y2", PinType.OC),
        6: Pin("1Y1", PinType.OC),
        7: Pin("1Y0", PinType.OC),
        9: Pin("2Y0", PinType.OC),
        10: Pin("2Y1", PinType.OC),
        11: Pin("2Y2", PinType.OC),
        12: Pin("2Y3", PinType.OC),
        13: Pin("A", PinType.IN),
        14: Pin("~2G", PinType.IN),
        15: Pin("~2C", PinType.IN),
    }

    # 74156 OC outputs are too slow to run full-speed with 5k pull-ups
    read_delay_us = 0.4
    default_inputs = [3, 13,  2, 1,  14, 15]
    default_outputs = [4, 5, 6, 7,  12, 11, 10, 9]

    test_inhibit = TestLogic("Inhibit", default_inputs, default_outputs,
        read_delay_us=read_delay_us,
        body=[
            [[*addr, 1, data, 1, data],  8*[1]]
            for addr in BV.range(0, 4)
            for data in [0, 1]
        ]
    )
    test_select_0 = TestLogic("Select 0", default_inputs, default_outputs,
        read_delay_us=read_delay_us,
        body=[
            [[*BV.int(addr, 2), 0, 0,  0, 0],  [1, 1, 1, 1, *~BV.bit(addr, 4)]] for addr in range(0, 4)
        ]
    )
    test_select_1 = TestLogic("Select 1", default_inputs, default_outputs,
        read_delay_us=read_delay_us,
        body=[
            [[*BV.int(addr, 2), 0, 1,  0, 1],  [*~BV.bit(addr, 4), 1, 1, 1, 1]] for addr in range(0, 4)
        ]
    )

    tests = [test_select_0, test_select_1, test_inhibit]
