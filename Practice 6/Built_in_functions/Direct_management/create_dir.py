import os

files = os.listdir("Practice 6/Built_in_functions/Direct_management/dir1_dir2")

for f in files:
    if f.endswith(".txt"):
        print(f)
