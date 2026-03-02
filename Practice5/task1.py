import re

pattern = r"^ab*$"

text = input("Enter a string: ")

if re.match(pattern, text):
    print("Match found")
else:
    print("No match")
