import os
from functions.get_file_content import get_file_contents

tests = [
    ("Reading 'main.py':", "calculator", "main.py"),
    ("Reading 'pkg/calculator.py':", "calculator", "pkg/calculator.py"),
    ("Reading file outside working directory:", "calculator", "/bin/cat"),
    ("Reading a non-existent file:", "calculator", "pkg/does_not_exist.py")
]

# tests = [("Read 'lorem.txt'", "calculator", "lorem.txt")]

for label, wd, file_path in tests:
    print(f"\n{label}")
    result = get_file_contents(working_directory=wd, file_path=file_path)
    print(result)