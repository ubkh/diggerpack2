import os

def check_for_suspicious_lines(file_path):
    """
    Checks a file for lines that might be missing an equals sign.
    """
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # A simple check for a single quote that isn't part of a value definition
            if "'" in line and '=' not in line and 'mc-versions' not in line:
                print(f"Suspicious line found in {file_path} on line {i+1}: {line.strip()}")
                return
            
def main():
    mods_dir = 'mods'
    
    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            check_for_suspicious_lines(file_path)

if __name__ == "__main__":
    main()