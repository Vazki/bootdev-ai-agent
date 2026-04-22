import os
from functions.write_file import write_file

tests = [
    ("Writing to 'lorem.txt':", "calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("Writing to a non-existent file:", "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("Writing to a file outside working directory:", "calculator", "/tmp/temp.txt", "this should not be allowed")
]

for label, wd, file_path, content in tests:
    print(f"\n{label}")
    result = write_file(working_directory=wd, file_path=file_path, content=content)
    print(result)