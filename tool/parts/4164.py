from prototypes import (PackageDIP16_rotated, Pin, PinType, Test)

class Part4164(PackageDIP16_rotated):
    SIZE_64 = 1
    SIZE_256 = 2
    MEM_TEST_SPEED = 0
    MEM_TEST_MARCH_C_MINUS_RMW = 1
    MEM_TEST_MARCH_C_MINUS_RW = 2
    MEM_TEST_MARCH_C_MINUS_PAGE = 3

    name = "4164"
    desc = "65536 x 1bit DRAM memory"
    pin_cfg = {
        1: Pin("NC", PinType.NC),
        2: Pin("Din", PinType.IN),
        3: Pin("~WE", PinType.IN),
        4: Pin("~RAS", PinType.IN),
        5: Pin("A0", PinType.IN),
        6: Pin("A2", PinType.IN),
        7: Pin("A1", PinType.IN),
        9: Pin("A7", PinType.IN),
        10: Pin("A5", PinType.IN),
        11: Pin("A4", PinType.IN),
        12: Pin("A3", PinType.IN),
        13: Pin("A6", PinType.IN),
        14: Pin("Dout", PinType.ST3),
        15: Pin("~CAS", PinType.IN),
    }

    default_inputs = [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15]
    default_outputs = [14]

    tests = [
        Test("MARCH C- Read-Modify-Write mode", Test.DRAM, default_inputs, default_outputs,
            params=[SIZE_64, MEM_TEST_MARCH_C_MINUS_RMW],
            loops=1,
        ),
        Test("MARCH C- Read+Write mode", Test.DRAM, default_inputs, default_outputs,
            params=[SIZE_64, MEM_TEST_MARCH_C_MINUS_RW],
            loops=1,
        ),
        Test("MARCH C- Page access mode", Test.DRAM, default_inputs, default_outputs,
            params=[SIZE_64, MEM_TEST_MARCH_C_MINUS_PAGE],
            loops=1,
        ),
        Test("CAS-Dout delay (use oscilloscope)", Test.DRAM, default_inputs, default_outputs,
            params=[SIZE_64, MEM_TEST_SPEED],
            loops=1,
        ),
    ]
