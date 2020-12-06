from typing import List


class NoTyping:
    def __init__(self, a, b):
        self._a = a
        self._b = b


class SomeTyping:
    def __init__(self, no_typing: NoTyping, b):
        self._no_typing = no_typing
        self._b = b


class A:
    pass


class B:
    def __init__(self, a: A):
        self.a = a


class C:
    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b


class ParentClass:
    def __init__(self, b: B):
        self._b = b

    def a_method(self):
        pass


class SubClass(ParentClass):
    def __init__(self, c: C, b: B):
        super().__init__(b)
        self._c = c


class UsesSubClass:
    def __init__(self, pc: ParentClass):
        self._pc = pc


class Base:
    def test(self):
        pass


class Impl1(Base):
    pass


class Impl2(Base):
    pass


class UsesMultiple:
    def __init__(self, multiple: List[Base]):
        self._multiple = multiple


class UsesBase:
    def __init__(self, base: Base):
        self._base = base
