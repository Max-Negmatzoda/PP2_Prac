import math


# 1️⃣ Degree → Radian (готовая функция)
degree = float(input("Input degree: "))
print("Output radian:", math.radians(degree))


print()


# 2️⃣ Area of trapezoid
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
print("Expected Output:", 0.5 * (base1 + base2) * height)


print()


# 3️⃣ Area of regular polygon (math.tan и math.pi)
n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))
area = (n * side**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)


print()


# 4️⃣ Area of parallelogram
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
print("Expected Output:", base * height)
