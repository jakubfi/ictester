from binvec import BV
from part import (PackageDIP20, Pin, PinType, ZIFFunc)
from test import TestLogic

in_out_hiz = [ZIFFunc.OUT, ZIFFunc.IN_PU_WEAK, ZIFFunc.IN_PU_STRONG]
out_in_hiz = [ZIFFunc.IN_PU_WEAK, ZIFFunc.OUT, ZIFFunc.IN_PU_STRONG]

class Part74S245(PackageDIP20):
    name = "74S245"
    desc = "Octal Bus Transceivers With 3-State Outputs"
    pin_cfg = {
        1: Pin("DIR", PinType.IN),
        2: Pin("A1", PinType.BIDI, zif_func=in_out_hiz),
        3: Pin("A2", PinType.BIDI, zif_func=in_out_hiz),
        4: Pin("A3", PinType.BIDI, zif_func=in_out_hiz),
        5: Pin("A4", PinType.BIDI, zif_func=in_out_hiz),
        6: Pin("A5", PinType.BIDI, zif_func=in_out_hiz),
        7: Pin("A6", PinType.BIDI, zif_func=in_out_hiz),
        8: Pin("A7", PinType.BIDI, zif_func=in_out_hiz),
        9: Pin("A8", PinType.BIDI, zif_func=in_out_hiz),
        11: Pin("B8", PinType.BIDI, zif_func=out_in_hiz),
        12: Pin("B7", PinType.BIDI, zif_func=out_in_hiz),
        13: Pin("B6", PinType.BIDI, zif_func=out_in_hiz),
        14: Pin("B5", PinType.BIDI, zif_func=out_in_hiz),
        15: Pin("B4", PinType.BIDI, zif_func=out_in_hiz),
        16: Pin("B3", PinType.BIDI, zif_func=out_in_hiz),
        17: Pin("B2", PinType.BIDI, zif_func=out_in_hiz),
        18: Pin("B1", PinType.BIDI, zif_func=out_in_hiz),
        19: Pin("~OE", PinType.IN),
    }

    tests = [
        TestLogic("A->B",
            cfgnum=0, # A: inputs, B: outputs
            loops=512,
            inputs=[1, 19,  2, 3, 4, 5, 6, 7, 8, 9],
            outputs=[18, 17, 16, 15, 14, 13, 12, 11],
            body=[[[1, 0, *v], v] for v in BV.range(0, 256)]
        ),
        TestLogic("B->A",
            cfgnum=1, # A: outputs, B: inputs
            loops=512,
            inputs=[1, 19,  18, 17, 16, 15, 14, 13, 12, 11],
            outputs=[2, 3, 4, 5, 6, 7, 8, 9],
            body=[[[0, 0, *v], v] for v in BV.range(0, 256)]
        ),
        TestLogic("A/B HiZ",
            cfgnum=2, # A and B: HiZ, pulled up strong
            inputs=[1, 19],
            outputs=[18, 17, 16, 15, 14, 13, 12, 11, 2, 3, 4, 5, 6, 7, 8, 9],
            body=[
                [[1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            ]
        ),
    ]
