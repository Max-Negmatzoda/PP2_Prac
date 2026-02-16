# Example 1 — local variable
def test():
    x = 10
    print(x)
test()


# Example 2 — global variable
x = 5
def show():
    print(x)
show()


# Example 3 — change global variable
count = 0
def inc():
    global count
    count += 1
inc()
print(count)


# Example 4 — enclosing scope
def outer():
    x = 10
    def inner():
        print(x)
    inner()
outer()


# Example 5 — nonlocal keyword
def outer():
    x = 1
    def inner():
        nonlocal x
        x += 1
    inner()
    print(x)
outer()
