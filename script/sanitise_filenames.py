import os
import sys
import toml
import re

# Get the path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.append(parent_dir)

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
    print("Sanitizing filenames...")
    for directory in SANITISE_DIRS:
        print(f"Processing directory: {directory}")
        sanitize_and_update_filenames(directory)
    print("Finished sanitizing filenames in all specified directories.")

if __name__ == "__main__":
    main()