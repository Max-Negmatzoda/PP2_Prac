# enumerate() - returns index and element while iterating through a list

names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names):
    print(index, name)


# zip() - combines elements from multiple lists by position

names_ = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 88]

for name_, score in zip(names_, scores):
    print(name_, score)


# map() - applies a function to every element in a list
# filter() - selects elements that satisfy a condition

numbers = [1, 2, 3, 4, 5]
numbers2 = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x**2, numbers))
even = list(filter(lambda x: x % 2 == 0, numbers2))

print(squared)
print(even)


# reduce() - applies a function cumulatively to reduce a list to one value

from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, numbers)

print(result)


# int() - converts a value to an integer
# type() - returns the type of an object

x = 10

num_str = "123"
num = int(num_str)

print(type(x))
print(num)
print(type(num))
