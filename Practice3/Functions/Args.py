# Example 1 — *args collects positional arguments
def add_all(*numbers):
    print(sum(numbers))
add_all(1, 2, 3, 4)


# Example 2 — loop through *args
def show_args(*args):
    for a in args:
        print(a)
show_args("a", "b", "c")


# Example 3 — **kwargs collects keyword arguments
def show_info(**info):
    print(info)
show_info(name="Max", age=16)


# Example 4 — loop through **kwargs
def print_pairs(**data):
    for k, v in data.items():
        print(k, v)
print_pairs(x=10, y=20)


# Example 5 — mix normal + args + kwargs
def mix(a, *args, **kwargs):
    print(a, args, kwargs)
mix(1, 2, 3, name="Max")
