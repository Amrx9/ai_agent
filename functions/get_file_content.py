import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    combiend_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(combiend_path)
    
    if not full_path.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        MAX_CHARS = 10000

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read(MAX_CHARS)
        except UnicodeDecodeError:
            return "Error: This is not a valid text file (not UTF-8)."
        
        if len(content) == MAX_CHARS:
            return content[:MAX_CHARS] + f'[...File "{full_path}" truncated at 10000 characters]'
        else:
            return content

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {10000} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)