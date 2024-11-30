import inspect
import sys
from os.path import dirname, basename, isfile, join
import glob

__all__ = [
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "part_*.py"))
    if isfile(f)
]

from . import *

catalog = {}
for i in inspect.getmembers(sys.modules["parts"], lambda x: inspect.ismodule(x)):
    for j in inspect.getmembers(i[1], lambda x: inspect.isclass(x) and x.__name__.startswith("Part")):
        catalog[j[1].name.upper()] = j[1]()
