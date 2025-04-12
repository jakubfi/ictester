from enum import Enum

CmdType = Enum("Cmd",
    names=[
        ("HELLO", 1),
        ("DUT_SETUP", 2),
        ("DUT_POWERUP", 3),
        ("TEST_SETUP", 4),
        ("VECTORS_LOAD", 5),
        ("RUN", 6),
        ("DUT_DISCONNECT", 7),
    ]
)

