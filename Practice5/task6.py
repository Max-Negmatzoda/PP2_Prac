import re

text = input("Enter text: ")

result = re.sub(r"[ ,\.]", ":", text)

print("Result:", result)
