import os

def strip_toml_lines(file_path):
    """
    Reads a TOML file, strips specific lines, including multi-line arrays.
    """
    lines_to_keep = []
    skip_lines = False
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        stripped_line = line.strip()

        # Check for the start of the keys to be stripped
        if (stripped_line.startswith("x-prismlauncher-loaders") or
            stripped_line.startswith("x-prismlauncher-mc-versions") or
            stripped_line.startswith("x-prismlauncher-release-type")):
            
            # Check if the line is an array and set the skip_lines flag
            if '[' in stripped_line:
                skip_lines = True
            
            continue # Skip this line
        
        # If we are skipping lines due to a multi-line array, check for the end
        if skip_lines:
            if ']' in stripped_line:
                skip_lines = False
            continue # Skip this line
        
        lines_to_keep.append(line)

    with open(file_path, 'w') as file:
        file.writelines(lines_to_keep)
        
def main():
    """
    Iterates through all .pw.toml files in the 'mods' directory and strips the lines.
    """
    mods_dir = 'mods'
    
    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            print(f"Processing {file_path}...")
            strip_toml_lines(file_path)
            
    print("All specified lines have been stripped from .pw.toml files.")

if __name__ == "__main__":
    main()