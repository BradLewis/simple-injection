from simple_injection import ServiceCollection, ServiceResolverFlags, ServiceLifetime


class A:
    def test(self):
        print("testing")


a = ServiceCollection()
a.add_transient(A, A)

x = a.resolve(A)
x.test()
