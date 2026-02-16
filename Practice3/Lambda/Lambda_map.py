# Example 1 — double values
nums = [1, 2, 3]
print(list(map(lambda x: x * 2, nums)))


# Example 2 — square values
nums = [2, 3, 4]
print(list(map(lambda x: x**2, nums)))


# Example 3 — convert to string
nums = [1, 2, 3]
print(list(map(lambda x: str(x), nums)))


# Example 4 — add constant
nums = [5, 6, 7]
print(list(map(lambda x: x + 10, nums)))


# Example 5 — length of words
words = ["hi", "hello"]
print(list(map(lambda w: len(w), words)))
