# Example 1 — simple square
square = lambda x: x * x
print(square(4))  # returns 16


# Example 2 — add two numbers
add = lambda a, b: a + b
print(add(2, 3))  # returns 5


# Example 3 — no parameters
hello = lambda: "Hello"
print(hello())  # returns string


# Example 4 — conditional lambda
check = lambda x: "positive" if x > 0 else "negative"
print(check(-5))


# Example 5 — lambda inside variable
triple = lambda x: x * 3
print(triple(5))
