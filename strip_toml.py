import os

def strip_toml_lines(file_path):
    """
    Reads a TOML file, strips specific lines, and writes the changes back.
    """
    lines_to_keep = []
    
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if not (stripped_line.startswith("x-prismlauncher-loaders") or
                    stripped_line.startswith("x-prismlauncher-mc-versions") or
                    stripped_line.startswith("x-prismlauncher-release-type")):
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