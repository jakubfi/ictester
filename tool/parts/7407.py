from binvec import BV
from part import partimport
from test import TestLogic

class Part7407(partimport("7405")):
    name = "7407"
    desc = "Hex Buffers/Drivers With Open-Collector High-Voltage Outputs"

    tests = [
        TestLogic("Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            body=[[x, x] for x in BV.range(0, 2**6)]
        )
    ]
