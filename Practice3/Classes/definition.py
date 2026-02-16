# Example 1 — simple class
class Dog:
    pass


# Example 2 — class with attribute
class Cat:
    name = "Tom"
print(Cat.name)


# Example 3 — create object
class Car:
    brand = "Toyota"
c = Car()
print(c.brand)


# Example 4 — method inside class
class Hello:
    def say(self):
        print("Hi")
Hello().say()


# Example 5 — multiple objects
class Person:
    pass
p1 = Person()
p2 = Person()
print(type(p1))
