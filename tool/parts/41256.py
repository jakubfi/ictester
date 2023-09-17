from prototypes import (PackageDIP16_rotated, Pin, PinType, TestDRAM)

class Part41256(PackageDIP16_rotated):
    SIZE_64 = 1
    SIZE_256 = 2
    MEM_TEST_SPEED = 0
    MEM_TEST_MARCH_C_MINUS_RMW = 1
    MEM_TEST_MARCH_C_MINUS_RW = 2
    MEM_TEST_MARCH_C_MINUS_PAGE = 3

    name = "41256"
    desc = "262144 x 1bit DRAM memory"
    pin_cfg = {
        1: Pin("A8", PinType.IN),
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

    tests = [
        TestDRAM("MARCH C- Read-Modify-Write mode", MEM_TEST_MARCH_C_MINUS_RMW, SIZE_256),
        TestDRAM("MARCH C- Read+Write mode", MEM_TEST_MARCH_C_MINUS_RW, SIZE_256),
        TestDRAM("MARCH C- Page access mode", MEM_TEST_MARCH_C_MINUS_PAGE, SIZE_256),
        TestDRAM("CAS-Dout delay (use oscilloscope)", MEM_TEST_SPEED, SIZE_256),
    ]
