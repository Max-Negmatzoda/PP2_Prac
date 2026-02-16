# Example 1 — even numbers
nums = [1, 2, 3, 4]
print(list(filter(lambda x: x % 2 == 0, nums)))


# Example 2 — positive numbers
nums = [-2, 3, -1, 5]
print(list(filter(lambda x: x > 0, nums)))


# Example 3 — long words
words = ["hi", "python", "ok"]
print(list(filter(lambda w: len(w) > 2, words)))


# Example 4 — non zero values
nums = [0, 1, 0, 5]
print(list(filter(lambda x: x != 0, nums)))


# Example 5 — numbers > 10
nums = [5, 12, 7, 20]
print(list(filter(lambda x: x > 10, nums)))
