from simple_injection import ServiceCollection


class A:
    def test(self):
        print("testing")


a = ServiceCollection()
a.add_transient(A, A)

x = a.resolve(A)
x.test()
