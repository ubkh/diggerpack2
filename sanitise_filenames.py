import os
import toml
import re
from config import SANITISE_DIRS

def sanitize_and_update_filenames(directory):
    """
    Iterates through all .zip files in a directory, sanitizes their names,
    and renames the files.
    """
    if not os.path.exists(directory):
        print(f"Warning: Directory '{directory}' not found. Skipping.")
        return

    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            file_path = os.path.join(directory, filename)
            
            # Sanitize the filename
            sanitized_name = filename.replace(' ', '_')
            sanitized_name = re.sub(r'[\[\]]', '', sanitized_name)
            
            # Only rename if a change is needed
            if filename != sanitized_name:
                sanitized_path = os.path.join(directory, sanitized_name)
                os.rename(file_path, sanitized_path)
                
                print(f"Sanitized filename in {directory}:")
                print(f"  Original: {filename}")
                print(f"  Updated:  {sanitized_name}")

def main():
    print("--- Running Filename Sanitization ---")
    for directory in SANITISE_DIRS:
        print(f"Processing directory: {directory}")
        sanitize_and_update_filenames(directory)
    print("Finished sanitizing filenames in all specified directories.")

if __name__ == "__main__":
    main()