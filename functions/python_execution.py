import os
import subprocess
from typing import List, Optional
from google.genai import types


def validate_python_file(working_directory: str, file_path: str) -> Optional[str]:
    """Validate that the file is a Python file and exists within working directory."""
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    return None


def execute_python_subprocess(file_path: str, working_dir: str, 
                            args: Optional[List[str]] = None) -> subprocess.CompletedProcess:
    """Execute Python file as a subprocess."""
    command = ["python", file_path]
    if args:
        command.extend(args)
    
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=working_dir,
        check=True
    )


def format_execution_result(result: subprocess.CompletedProcess) -> str:
    """Format the execution result into a readable string."""
    if result.stdout == "" and result.stderr == "":
        return "No output produced."
    
    output_parts = []
    if result.stdout:
        output_parts.append(f"STDOUT: {result.stdout}")
    if result.stderr:
        output_parts.append(f"STDERR: {result.stderr}")
    
    return "\n".join(output_parts)


def handle_execution_error(error: Exception) -> str:
    """Handle different types of execution errors."""
    if isinstance(error, subprocess.CalledProcessError):
        return (f"STDOUT: {error.stdout}\n"
                f"STDERR: {error.stderr}\n"
                f"Process exited with code {error.returncode}")
    elif isinstance(error, subprocess.TimeoutExpired):
        return "Command timed out!"
    else:
        return f"Error executing Python file: {error}"


def run_python_file(working_directory: str, file_path: str, 
                   args: Optional[List[str]] = None) -> str:
    """Execute a Python file and return the output."""
    # Validate the file
    validation_error = validate_python_file(working_directory, file_path)
    if validation_error:
        return validation_error
    
    abs_working_dir = os.path.abspath(working_directory)
    
    try:
        result = execute_python_subprocess(file_path, abs_working_dir, args)
        return format_execution_result(result)
        
    except Exception as e:
        return handle_execution_error(e)


# Schema definition
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)