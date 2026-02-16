# Example 1 — instance method
class A:
    def show(self):
        print("Instance method")
A().show()


# Example 2 — class method
class B:
    count = 0
    @classmethod
    def show(cls):
        print(cls.count)
B.show()


# Example 3 — static method
class C:
    @staticmethod
    def add(a, b):
        return a + b
print(C.add(2, 3))


# Example 4 — modify class variable
class D:
    x = 0
    @classmethod
    def inc(cls):
        cls.x += 1
D.inc()
print(D.x)


# Example 5 — utility static method
class Math:
    @staticmethod
    def square(x):
        return x*x
print(Math.square(5))
