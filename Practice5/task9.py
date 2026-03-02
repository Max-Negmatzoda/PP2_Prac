import re

text = input("Enter text: ")

result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

print(result)
