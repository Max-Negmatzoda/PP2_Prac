import shutil

# copy file
shutil.copy(
    "Practice 6/Built_in_functions/Direct_management/dir1_dir2/file.txt",
    "Practice 6/Built_in_functions/Direct_management/file_copy.txt"
)

# move file
shutil.move(
    "Practice 6/Built_in_functions/Direct_management/dir1_dir2/file.txt",
    "Practice 6/Built_in_functions/Direct_management/file_moved.txt"
)
