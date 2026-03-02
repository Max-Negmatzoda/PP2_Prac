import re

text = input("Enter camelCase: ")

result = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

print(result)
