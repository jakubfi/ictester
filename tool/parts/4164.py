from prototypes import (PackageDIP16_rotated, Pin, PinType, TestDRAM, DRAMType, DRAMTestType)

class Part4164(PackageDIP16_rotated):
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

    tests = [
        TestDRAM("MARCH C- Read-Modify-Write mode", DRAMType.DRAM_4164, DRAMTestType.MARCH_C_MINUS_RMW),
        TestDRAM("MARCH C- Read+Write mode", DRAMType.DRAM_4164, DRAMTestType.MARCH_C_MINUS_RW),
        TestDRAM("MARCH C- Page access mode", DRAMType.DRAM_4164, DRAMTestType.MARCH_C_MINUS_PAGE),
        TestDRAM("CAS-Dout delay (use oscilloscope)", DRAMType.DRAM_4164, DRAMTestType.SPEED_CHECK),
    ]
