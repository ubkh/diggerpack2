import os

def strip_toml_lines(file_path):
    """
    Reads a TOML file, strips specific lines, and writes the changes back.
    """
    lines_to_keep = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # Check for the start of the keys to be stripped
        if (stripped_line.startswith("x-prismlauncher-loaders") or
            stripped_line.startswith("x-prismlauncher-mc-versions") or
            stripped_line.startswith("x-prismlauncher-release-type")):
            
            # This is the line we want to remove. Now, check if it's an array.
            if '[' in stripped_line:
                # If it's an array, we need to skip lines until we find the closing bracket.
                i += 1
                while i < len(lines):
                    current_line = lines[i].strip()
                    if ']' in current_line:
                        break # Found the end of the array, so we stop skipping.
                    i += 1
            # In all cases, we continue to the next line to avoid adding the key line itself.
            i += 1
            continue

        lines_to_keep.append(line)
        i += 1

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