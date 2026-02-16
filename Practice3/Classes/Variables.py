# Example 1 — shared variable
class Dog:
    species = "Canine"
print(Dog.species)


# Example 2 — access via object
d = Dog()
print(d.species)


# Example 3 — change class variable
Dog.species = "Animal"
print(Dog.species)


# Example 4 — instance override
d.species = "Pet"
print(d.species)
print(Dog.species)


# Example 5 — counter
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
Counter()
Counter()
print(Counter.count)
