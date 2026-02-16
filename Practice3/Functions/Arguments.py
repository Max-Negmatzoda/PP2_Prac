# Example 1 — positional argument
def greet(name):
    print("Hello", name)
greet("Max")


# Example 2 — default argument
def power(base, exp=2):
    print(base ** exp)
power(5)


# Example 3 — keyword arguments
def info(name, age):
    print(name, age)
info(age=16, name="Alex")


# Example 4 — multiple arguments
def sum3(a, b, c):
    print(a + b + c)
sum3(1, 2, 3)


# Example 5 — optional argument
def print_user(name="Guest"):
    print(name)
print_user()
