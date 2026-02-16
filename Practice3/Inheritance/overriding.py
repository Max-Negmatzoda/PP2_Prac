# Example 1 — override method
class A:
    def speak(self):
        print("A")

class B(A):
    def speak(self):
        print("B")


# Example 2 — different behavior
class Animal:
    def sound(self):
        print("Some sound")

class Dog(Animal):
    def sound(self):
        print("Bark")


# Example 3 — override with extra logic
class P:
    def show(self):
        print("Parent")

class C(P):
    def show(self):
        print("Child first")


# Example 4 — polymorphism
for obj in [Animal(), Dog()]:
    obj.sound()


# Example 5 — override return value
class X:
    def val(self):
        return 1

class Y(X):
    def val(self):
        return 2
print(Y().val())
