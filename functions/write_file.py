import os


def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(full_path):
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
            
        except Exception as e:
            return f"Error: {e}"
