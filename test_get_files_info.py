from functions.get_files_info import get_files_info

tests = [
    ("List files in '.'",       "calculator", "."),
    ("List files in 'pkg'",     "calculator", "pkg"),
    ("List files in '/bin'",    "calculator", "/bin"),
    ("List files in '../'",     "calculator", "../")
]

for label, wd, directory in tests:
    print(f"\n{label}")
    result = get_files_info(working_directory=wd, directory=directory)
    if result:
        print("\n".join(result) if isinstance(result, list) else result)