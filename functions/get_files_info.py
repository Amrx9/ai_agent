import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    abs_working = os.path.abspath(working_directory)
    
    if directory:
        combined_path = os.path.join(working_directory, directory)
        abs_directory = os.path.abspath(combined_path)
    else:
        abs_directory = abs_working

    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(abs_directory)
        result_lines = []
        
        for file in contents:
            full_path = os.path.join(abs_directory, file)
            line = f"- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
            result_lines.append(line)
            
        return "\n".join(result_lines)
    
    except OSError as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)