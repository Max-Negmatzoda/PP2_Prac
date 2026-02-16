# Example 1 — simple inheritance
class A:
    def hello(self):
        print("Hello")

class B(A):
    pass
B().hello()


# Example 2 — child adds method
class Animal:
    def eat(self):
        print("Eating")

class Dog(Animal):
    def bark(self):
        print("Bark")


# Example 3 — override attribute
class Parent:
    x = 1

class Child(Parent):
    x = 2
print(Child.x)


# Example 4 — check type
print(isinstance(Dog(), Animal))


# Example 5 — reuse methods
Dog().eat()
