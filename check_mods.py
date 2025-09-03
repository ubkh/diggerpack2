import os
import toml

def check_for_missing_keys(file_path):
    """
    Checks a .pw.toml file for missing required keys.
    """
    required_sections = ['download']
    required_keys = {
        'version': ['mod-id'],
        'download': ['url']
    }

    try:
        with open(file_path, 'r') as file:
            data = toml.load(file)

        for section in required_sections:
            if section not in data:
                print(f"Error: Missing section '[{section}]' in {file_path}")
                continue

            for key in required_keys[section]:
                if key not in data[section]:
                    print(f"Error: Missing key '{key}' in section '[{section}]' in {file_path}")

    except toml.TomlDecodeError as e:
        print(f"Error parsing TOML in {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with {file_path}: {e}")

def main():
    mods_dir = 'mods'
    
    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            print(f"Checking {file_path}...")
            check_for_missing_keys(file_path)
            
    print("Finished checking all files.")

if __name__ == "__main__":
    main()