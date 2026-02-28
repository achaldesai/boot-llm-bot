from os import path, listdir
from google.genai import types

schema_get_file_info = types.FunctionDeclaration(
    name="get_file_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_info(working_directory, directory="."):
    try:
        abs_working_path = path.abspath(working_directory)
        target_dir = path.normpath(path.join(abs_working_path, directory))
        valid_target_dir = (
            path.commonpath([abs_working_path, target_dir]) == abs_working_path
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        target_is_valid_dir = path.isdir(target_dir)
        if not target_is_valid_dir:
            return f'Error: "{directory}" is not a directory'
        list_target_dir = listdir(target_dir)
        mapped_target_dir = list(
            map(
                lambda x: f" - {x}: file_size={path.getsize('/'.join([target_dir, x]))} bytes, is_dir={path.isdir('/'.join([target_dir, x]))}",
                list_target_dir,
            )
        )
        return "\n".join(mapped_target_dir)

    except Exception as e:
        return f"Error: {e}"
