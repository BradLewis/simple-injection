from simple_injection import ServiceCollection


class A:
    def test(self):
        print("testing")


a = ServiceCollection()
a.add_transient(id(A), A)

x = a.resolve(id(A))
x.test()
