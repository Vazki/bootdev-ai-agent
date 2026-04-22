import os
from config import *
import google.genai.types as types

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
            
# Define the function declaration schema for get_file_content
# This should be added to the list of available functions in call_function.py
# Used for type checking and to provide metadata about the function to the agent
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)