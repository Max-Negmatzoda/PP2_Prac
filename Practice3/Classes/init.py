# Example 1 — basic constructor
class Person:
    def __init__(self, name):
        self.name = name
p = Person("Max")
print(p.name)


# Example 2 — multiple attributes
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year


# Example 3 — default value
class User:
    def __init__(self, name="Guest"):
        self.name = name
print(User().name)


# Example 4 — calculation
class Square:
    def __init__(self, side):
        self.area = side * side
print(Square(4).area)


# Example 5 — print in init
class Hello:
    def __init__(self):
        print("Created")
Hello()
