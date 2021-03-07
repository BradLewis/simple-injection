from simple_injection import ServiceCollection, ServiceResolverFlags
from time import time


class A:
    def __init__(self, i):
        self.i = i

    def test(self):
        print(f"testing {self.i}")


class B:
    def __init__(self, a: A):
        self.a = a
        print("test")

    def test(self):
        print("calling A!")
        self.a.test()


s = time()
for _ in range(1000):
    a = ServiceCollection()
    a.add_transient(A, args=[10])
    a.add_transient(B)

    x = a.resolve(B)
    x.test()
print(time() - s)
