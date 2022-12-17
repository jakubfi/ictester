from prototypes import (Test, partimport)

class Part7407(partimport("7405")):
    name = "7407"
    desc = "Hex Buffers/Drivers With Open-Collector High-Voltage Outputs"
    tests = [
        Test(
            name="Complete logic",
            inputs=[1, 3, 5, 9, 11, 13],
            outputs=[2, 4, 6, 8, 10, 12],
            ttype=Test.COMB,
            body=Test.binary_fun_gen(6, 1, lambda a: a)
        )
    ]