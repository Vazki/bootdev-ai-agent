import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, directory))

    if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
        return f'Error: Cannot list "{directory}" because it is outside the permitted working directory.'
    if not os.path.exists(target):
        return f'Error: The directory "{directory}" does not exist within the working directory.'
    if not os.path.isdir(target):
        return f'Error: The path "{directory}" is not a directory within the working directory.'

    try:
        return [
            f"{e}: file_size={os.path.getsize(os.path.join(target, e))}, is_dir={os.path.isdir(os.path.join(target, e))}"
            for e in os.listdir(target)
        ]
    except Exception as e:
        return f'Error: An error occurred while listing files in "{directory}": {str(e)}'
