from binvec import BV
from prototypes import (Test, partimport)

class Part7407(partimport("7405")):
    name = "7407"
    desc = "Hex Buffers/Drivers With Open-Collector High-Voltage Outputs"

    tests = [
        Test("Complete logic", Test.COMB,
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            body=[[6*x, 6*x] for x in BV.range(0, 2)]
        )
    ]
