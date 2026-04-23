import os
from functools import reduce
import google.genai.types as types

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

# Define the function declaration schema for write_file
# This should be added to the list of available functions in call_function.py
# Used for type checking and to provide metadata about the function to the agent    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)