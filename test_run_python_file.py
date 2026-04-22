from functions.run_python_file import run_python_file

tests = [
    ("Running 'main.py':", "calculator", "main.py"),
    ("Running 'main.py' with arguments:", "calculator", "main.py", ["3 + 5"]),
    ("Running 'tests.py':", "calculator", "tests.py"),
    ("Running '../main.py' (outside working directory):", "calculator", "../main.py"),
    ("Running a non-existent file:", "calculator", "nonexistent.py"),
    ("Running 'lorem.txt' (not a Python file):", "calculator", "lorem.txt")
]

for label, wd, file_path, *args in tests:
    print(f"\n{label}")
    result = run_python_file(working_directory=wd, file_path=file_path, args=args[0] if args else None)
    print(result)