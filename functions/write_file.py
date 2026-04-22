import os
from functools import reduce

def write_file(working_directory, file_path, content):
    # If the file_path is outside the working_directory, return error string.
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target):
        return f'Error: Cannot write to "{file_path}" because it is a directory'

    try:
        # Ensure the target directory exists
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: An error occurred while writing to the file "{file_path}": {str(e)}'