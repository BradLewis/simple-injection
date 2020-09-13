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
