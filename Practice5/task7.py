def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

text = input("Enter snake_case string: ")

print("CamelCase:", snake_to_camel(text))
