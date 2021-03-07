from simple_injection import ServiceCollection, ServiceResolverFlags, ServiceLifetime


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


a = ServiceCollection()
a.add_transient(A, args=[10])
a.add_transient(B)

x = a.resolve(B)
x.test()
