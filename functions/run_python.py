import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not os.path.splitext(file_path)[1] == ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        results = subprocess.run(
            ["python", f"{abs_file_path}"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
            check=True
        )
       
        if results.stdout == "" and results.stderr == "":
            return "No output produced." 
        
        return f"STDOUT: {results.stdout}\nSTDERR: {results.stderr}"
        

    except subprocess.CalledProcessError as e:
        return f"STDOUT: {e.stdout}\nSTDERR: {e.stderr}\nProcess exited with code {e.returncode}"
    
    except subprocess.TimeoutExpired:
        return "Command timed out!"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"