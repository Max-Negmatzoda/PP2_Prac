import re

text = input("Enter text: ")

result = re.findall(r'[A-Z][a-z]*', text)

print(result)
