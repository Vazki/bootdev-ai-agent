import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    # get absolute path of the target file
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # error handling for file path
    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target) or not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    # Run the Python file and capture output
    try:
        command = ["python", target]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            output += f"\nNo output produced"
        else:
            output += f"\nSTDOUT:\n{result.stdout}"
            output += f"\nSTDERR:\n{result.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"