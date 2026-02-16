# Example 1 — call parent constructor
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        super().__init__()


# Example 2 — pass arguments
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name):
        super().__init__(name)


# Example 3 — extend method
class P:
    def show(self):
        print("Parent")

class C(P):
    def show(self):
        super().show()
        print("Child")


# Example 4 — reuse logic
class Base:
    def calc(self, x):
        return x*2

class Sub(Base):
    def calc(self, x):
        return super().calc(x)+1


# Example 5 — simple demo
class X:
    def say(self):
        print("X")
class Y(X):
    def say(self):
        super().say()
