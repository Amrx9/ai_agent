from google.genai import types
from typing import Dict, Callable, Any

from .file_operations import (
    get_files_info, schema_get_files_info,
    get_file_content, schema_get_file_content,
    write_file, schema_write_file
)
from .python_execution import run_python_file, schema_run_python_file


def get_available_functions() -> types.Tool:
    """Return all available function declarations."""
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )


def get_function_registry() -> Dict[str, Callable]:
    """Return a mapping of function names to their implementations."""
    return {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }


def execute_function(function_call_part: Any, verbose: bool = False) -> types.Part:
    """Execute a function call and return the result."""
    func_name = function_call_part.name
    
    if verbose:
        print(f"Calling function: {func_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {func_name}")
    
    function_registry = get_function_registry()
    
    if func_name not in function_registry:
        return create_error_response(func_name, f"Unknown function: {func_name}")
    
    try:
        # Get the function and prepare arguments
        actual_func = function_registry[func_name]
        args = prepare_function_args(function_call_part.args)
        
        # Execute the function
        result = actual_func(**args)
        
        if verbose:
            print(f"-> {result}")
        
        return create_success_response(func_name, result)
        
    except Exception as e:
        error_msg = f"Error executing {func_name}: {str(e)}"
        return create_error_response(func_name, error_msg)


def prepare_function_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare function arguments by adding working directory."""
    prepared_args = args.copy()
    prepared_args["working_directory"] = "./calculator"
    return prepared_args


def create_success_response(func_name: str, result: Any) -> types.Part:
    """Create a successful function response."""
    return types.Part.from_function_response(
        name=func_name,
        response={"result": result}
    )


def create_error_response(func_name: str, error_msg: str) -> types.Part:
    """Create an error function response."""
    return types.Part.from_function_response(
        name=func_name,
        response={"error": error_msg}
    )