# Example 1 — sort numbers ascending
nums = [5, 1, 3]
print(sorted(nums, key=lambda x: x))


# Example 2 — sort descending
nums = [5, 1, 3]
print(sorted(nums, key=lambda x: -x))


# Example 3 — sort by length
words = ["a", "python", "hi"]
print(sorted(words, key=lambda w: len(w)))


# Example 4 — sort by second element
pairs = [(1, 3), (2, 1), (0, 5)]
print(sorted(pairs, key=lambda x: x[1]))


# Example 5 — sort by last digit
nums = [23, 15, 42]
print(sorted(nums, key=lambda x: x % 10))
