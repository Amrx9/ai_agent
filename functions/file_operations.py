import os
from typing import Optional
from google.genai import types


def validate_path_security(working_directory: str, file_path: str) -> Optional[str]:
    """Validate that the file path is within the working directory."""
    abs_working = os.path.abspath(working_directory)
    combined_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(combined_path)
    
    if not full_path.startswith(abs_working):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    return None


def get_files_info(working_directory: str, directory: Optional[str] = None) -> str:
    """List files in the specified directory with their information."""
    abs_working = os.path.abspath(working_directory)
    
    if directory:
        target_directory = os.path.join(working_directory, directory)
        abs_directory = os.path.abspath(target_directory)
        
        # Security check
        if not abs_directory.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        abs_directory = abs_working
    
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory or "."}" is not a directory'
    
    try:
        return format_directory_listing(abs_directory)
    except OSError as e:
        return f"Error: {e}"


def format_directory_listing(directory_path: str) -> str:
    """Format directory contents into a readable string."""
    contents = os.listdir(directory_path)
    result_lines = []
    
    for file in contents:
        full_path = os.path.join(directory_path, file)
        file_size = os.path.getsize(full_path)
        is_directory = os.path.isdir(full_path)
        
        line = f"- {file}: file_size={file_size} bytes, is_dir={is_directory}"
        result_lines.append(line)
    
    return "\n".join(result_lines)


def get_file_content(working_directory: str, file_path: str) -> str:
    """Read and return the content of a file."""
    # Security validation
    security_error = validate_path_security(working_directory, file_path)
    if security_error:
        return security_error
    
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        return read_file_with_limit(full_path)
    except Exception as e:
        return f"Error: {e}"


def read_file_with_limit(file_path: str, max_chars: int = 10000) -> str:
    """Read file content with a character limit."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(max_chars)
    except UnicodeDecodeError:
        return "Error: This is not a valid text file (not UTF-8)."
    
    if len(content) == max_chars:
        return content[:max_chars] + f'[...File "{file_path}" truncated at {max_chars} characters]'
    
    return content


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write content to a file."""
    # Security validation
    security_error = validate_path_security(working_directory, file_path)
    if security_error:
        return security_error
    
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error writing to file: {e}"


# Schema definitions
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the first 10000 characters of the content from a specified file within the working directory.",
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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the specified file path, creating the file if it does not exist. The path is relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path you will write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file. If the file does not exist, it will be created; otherwise, it will be overwritten",
            )
        },
        required=["file_path", "content"],
    ),
)