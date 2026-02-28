from os import path
from google.genai import types
import subprocess


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file specified at the file_pat(relative to the working) also passes the args as arguments to the function call. Returns the output of the execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file from relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Content to be written to the file specified at file_path(default is [] empty list, no arguments will be passed)",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_path = path.abspath(working_directory)
        abs_file_path = path.normpath(path.join(abs_working_path, file_path))

        valid_file_path = (
            path.commonpath([abs_working_path, abs_file_path]) == abs_working_path
        )
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        is_valid_file = path.isfile(abs_file_path)
        if not is_valid_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        is_python_file = file_path.split(".")[-1] == "py"
        if not is_python_file:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", abs_file_path]
        completed_process_object = subprocess.run(
            [*command, *args],
            text=True,
            timeout=30,
            capture_output=True,
        )

        output_string = []
        if not completed_process_object.returncode == 0:
            output_string.append(
                f"Process exited with code {completed_process_object.returncode}"
            )

        if not completed_process_object.stderr and not completed_process_object.stdout:
            output_string.append("No output produced")

        if completed_process_object.stderr:
            output_string.append(f"STDERR:{completed_process_object.stderr}")
        if completed_process_object.stdout:
            output_string.append(f"STDOUT:{completed_process_object.stdout}")

        return "\n".join(output_string)
    except Exception as e:
        return f"Error: {e}"
