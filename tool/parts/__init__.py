__all__ = [
    "4164",
    "7400", "7402", "7403", "7404", "7405", "7406", "7407", "7408",
    "7410", "7411", "7412", "7413",
    "7420", "7421",
    "7430", "7432", "7437", "7438",
    "7440", "7442", "7445", "7447",
    "7450", "7451", "7452", "7453", "74h53",
    "7460", "7462",
    "7472", "7473", "7474", "7475",
    "7483", "7486", "7487", "7489",
    "7490", "7493", "7495", "7496",
    "74107",
    "74125", "74126",
    "74132", "74136",
    "74145", "74148",
    "74150", "74151", "74153", "74154", "74155", "74156", "74157",
    "74161", "74164", "74165", "74166",
    "74170", "74174", "74175",
    "74180", "74181", "74182",
    "74194", "74198",
    "74s201",
    "74s405",
    "780101",
]

import inspect
import sys
import re

from . import *

class Catalog:
    def __init__(self):
        self.parts = {}
        for i in inspect.getmembers(sys.modules["parts"], lambda x: inspect.ismodule(x)):
            for j in inspect.getmembers(i[1], lambda x: inspect.isclass(x) and x.__name__.startswith("Part")):
                self.parts[j[1].name] = j[1]()

    def names(self):
        return sorted(self.parts, key=lambda t: int(re.sub("74[HS]", "74", t[0])))

    def part(self, name):
        return self.parts[name]

catalog = Catalog()