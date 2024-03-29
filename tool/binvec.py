from functools import reduce

class BV(list):
    def __init__(self, vector, carry=0):
        self.carry = carry
        super().__init__(map(bool, vector))

    @classmethod
    def int(cls, val, length):
        binval = (
            (val >> (length-pos-1)) & 1
            for pos in range(0, length)
        )
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

    def even(self):
        return reduce(lambda a, b: a==b, self)

    def odd(self):
        return not self.even()

    def reversed(self):
        return BV(reversed(self))

    def vand(self):
        return reduce(lambda x, y: x and y, self)

    def vor(self):
        return reduce(lambda x, y: x or y, self)

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
        return BV(map(lambda x, y: x and y, self, obj))

    def __or__(self, obj):
        return BV(map(lambda x, y: x or y, self, obj))

    def __xor__(self, obj):
        return BV(map(lambda x, y: x != y, self, obj))

    def __lt__(self, obj):
        return int(self) < int(BV(obj))

    def __gt__(self, obj):
        return int(self) > int(BV(obj))

    def __str__(self):
        strvec = [int(v) for v in self]
        return str(strvec)

    def __int__(self):
        p = 1
        x = 0
        for i in reversed(self):
            x += i * p
            p *= 2
        x += self.carry * p
        return x

    def __bytes__(self):
        val = int(self)
        return bytes([(val >> shift) & 0xff for shift in range(0, len(self), 8)])
