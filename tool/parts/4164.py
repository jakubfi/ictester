from prototypes import (PackageDIP16_rotated, Pin, Test)

class Part4164(PackageDIP16_rotated):
    TEST_BIT_ALL_0 = 0
    TEST_BIT_ALL_1 = 1
    TEST_ROW_ALL_0 = 2
    TEST_ROW_ALL_1 = 3
    TEST_ROW_ALTERNATE_01 = 4
    TEST_ROW_ALTERNATE_10 = 5

    name = "4164"
    desc = "(also HM4864, ...) (REVERSE CHIP ORIENTATION!) 65536 x 1bit DRAM memory"
    pin_cfg = {
        1: Pin("NC", Pin.NC),
        2: Pin("Din", Pin.IN),
        3: Pin("~WE", Pin.IN),
        4: Pin("~RAS", Pin.IN),
        5: Pin("A0", Pin.IN),
        6: Pin("A2", Pin.IN),
        7: Pin("A1", Pin.IN),
        9: Pin("A7", Pin.IN),
        10: Pin("A5", Pin.IN),
        11: Pin("A4", Pin.IN),
        12: Pin("A3", Pin.IN),
        13: Pin("A6", Pin.IN),
        14: Pin("Dout", Pin.OUT),
        15: Pin("~CAS", Pin.IN),
    }
    test_bit_all_0 = Test(
        name="Single bit: all 0s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_BIT_ALL_0,
        loops=1,
    )
    test_bit_all_1 = Test(
        name="Single bit: all 1s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_BIT_ALL_1,
        loops=1,
    )
    test_row_all_0 = Test(
        name="Page mode: all 0s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALL_0,
        loops=1,
    )
    test_row_all_1 = Test(
        name="Page mode: all 1s",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALL_1,
        loops=1,
    )
    test_row_alternate_01 = Test(
        name="Page mode: alternating 0/1",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALTERNATE_01,
        loops=1,
    )
    test_row_alternate_10 = Test(
        name="Page mode: alternating 1/0",
        inputs=[2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],
        outputs=[14],
        ttype=Test.MEM,
        tsubtype=TEST_ROW_ALTERNATE_10,
        loops=1,
    )

    tests = [
        test_bit_all_0, test_bit_all_1,
        test_row_all_0, test_row_all_1,
        test_row_alternate_01, test_row_alternate_10
    ]
