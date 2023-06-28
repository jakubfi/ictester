from functools import reduce

class BV(list):
    def __init__(self, vector, carry=0):
        self.carry = carry
        super().__init__(int(bool(i)) for i in vector)

    @classmethod
    def int(cls, val, length):
        binval = [
            bool((val >> (length-pos-1)) & 1)
            for pos in range(0, length)
        ]
        carry = True if val & (2**length) else False
        return cls(binval, carry)

    @classmethod
    def bit(cls, position, length):
        return cls.int(1<<position, length)

    @classmethod
    def range(cls, start, stop):
        length = len(bin(stop-1)) - 2  # sorry
        return (
            cls.int(v, length)
            for v in range(start, stop)
        )

    def reversed(self):
        return BV(reversed(self))

    def vand(self):
        return BV([reduce(lambda x, y: x & y, self)])

    def vor(self):
        return BV([reduce(lambda x, y: x | y, self)])

    def __invert__(self):
        return BV(map(lambda x: not x, self))

    def __add__(self, obj):
        return BV.int(int(self) + int(obj), len(self))

    def __sub__(self, obj):
        raise RuntimeError("There is no such thing as binary subtraction ;-)")

    def __mul__(self, obj):
        return BV(list(self) * obj)

    def __rmul__(self, obj):
        return BV(list(self) * obj)

    def __and__(self, obj):
        return BV.int(int(self) & int(obj), len(self))

    def __or__(self, obj):
        return BV.int(int(self) | int(obj), len(self))

    def __xor__(self, obj):
        return BV.int(int(self) ^ int(obj), len(self))

    def __str__(self):
        strvec = ''.join(str(int(v)) for v in self)
        return f"[{strvec}]"

    def __int__(self):
        p = 0
        x = 0
        for i in list(reversed(self)) + [self.carry]:
            x += i * 2**p
            p += 1
        return x
