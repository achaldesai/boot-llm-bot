from os import path
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Gets contents of a file from the file path relative to the working directory, providing file content up to a limit of {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file from relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        abs_working_path = path.abspath(working_directory)
        abs_file_path = path.normpath(path.join(abs_working_path, file_path))

        valid_file_path = (
            path.commonpath([abs_working_path, abs_file_path]) == abs_working_path
        )
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        is_valid_file = path.isfile(abs_file_path)
        if not is_valid_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content
    except Exception as e:
        return f"Error: {e}"
