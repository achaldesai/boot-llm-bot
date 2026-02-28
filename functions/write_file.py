from os import path, makedirs
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes contents to a file at the file path relative to the working directory, the content is overwritten to the file not appended",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file from relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file specified at file_path",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        abs_working_path = path.abspath(working_directory)
        target_filepath = path.normpath(path.join(abs_working_path, file_path))

        valid_target_filepath = (
            path.commonpath([abs_working_path, target_filepath]) == abs_working_path
        )
        if not valid_target_filepath:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        target_is_valid_dir = path.isdir(target_filepath)
        if target_is_valid_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        makedirs("/".join(target_filepath.split("/")[:-1]), exist_ok=True)

        with open(target_filepath, "w") as f:
            f.write(content)
            return f'Successully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
