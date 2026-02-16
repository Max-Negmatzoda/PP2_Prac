# Example 1 — inherit from two classes
class A:
    def a(self): print("A")

class B:
    def b(self): print("B")

class C(A, B):
    pass
c = C()
c.a()
c.b()


# Example 2 — method resolution order
print(C.__mro__)


# Example 3 — override same method
class X:
    def show(self): print("X")

class Y:
    def show(self): print("Y")

class Z(X, Y):
    pass
Z().show()


# Example 4 — mix features
class Fly:
    def fly(self): print("Flying")

class Swim:
    def swim(self): print("Swimming")

class Duck(Fly, Swim):
    pass


# Example 5 — use both parents
d = Duck()
d.fly()
d.swim()
