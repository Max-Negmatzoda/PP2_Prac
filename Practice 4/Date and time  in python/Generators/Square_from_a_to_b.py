def gen_squares(n): #1
    for i in range(n + 1):
        yield i * i

for x in gen_squares(5):
    print(x)

#2
n = int(input())

def even_nums(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(map(str, even_nums(n))))

#3
def div_3_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

for x in div_3_4(100):
    print(x)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for x in squares(2, 6):
    print(x)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for x in countdown(5):
    print(x)

