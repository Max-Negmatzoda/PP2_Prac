# Example 1 — simple decorator
def deco(func):
    def wrapper():
        print("Before")
        func()
    return wrapper

@deco
def hello():
    print("Hello")
hello()


# Example 2 — decorator with return
def double(func):
    def wrapper():
        return func() * 2
    return wrapper

@double
def num():
    return 5
print(num())


# Example 3 — decorator with args
def log(func):
    def wrapper(x):
        print("Call")
        return func(x)
    return wrapper

@log
def square(x):
    return x * x
print(square(3))


# Example 4 — timing decorator
import time
def timer(func):
    def wrapper():
        start = time.time()
        func()
        print(time.time() - start)
    return wrapper


# Example 5 — multiple decorators
def bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper
