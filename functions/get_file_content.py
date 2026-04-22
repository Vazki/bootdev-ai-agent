import os
from config import *

def get_file_content(working_directory, file_path):
    # If the file_path is outside the working_directory, return error string.
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target):
        return f'Error: The file "{file_path}" does not exist within the working directory.'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target, 'r') as f:
            # Read up to MAX_CHARS characters to prevent reading very large files
            contents = f.read(MAX_CHARS)
            if f.read(1):  # Check if there are more characters after reading MAX_CHARS
                contents += f"\n[...File {file_path} truncated after {MAX_CHARS} characters...]"
            return contents
    except Exception as e:
        return f'Error: An error occurred while reading the file "{file_path}": {str(e)}'
            

