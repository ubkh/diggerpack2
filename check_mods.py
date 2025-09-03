import os
import toml
import urllib.parse

def check_for_malformed_url(file_path, data):
    """
    Checks if a download URL is malformed due to unencoded characters.
    """
    if 'download' in data and 'url' in data['download']:
        url = data['download']['url']
        
        # Check for unencoded characters that should be percent-encoded
        if ' ' in url or '[' in url or ']' in url:
            print(f"Warning: Malformed URL found in {file_path}")
            print(f"Reason: URL contains unencoded spaces or brackets.")
            print(f"URL: {url}")
            return True
    return False

def check_for_missing_keys(file_path, data):
    """
    Checks a .pw.toml file for missing required keys.
    """
    required_sections = ['download']
    required_keys = {
        'download': ['url']
    }
    
    issues_found = False

    for section in required_sections:
        if section not in data:
            print(f"Error: Missing section '[{section}]' in {file_path}")
            issues_found = True
            continue

        for key in required_keys[section]:
            if key not in data[section]:
                print(f"Error: Missing key '{key}' in section '[{section}]' in {file_path}")
                issues_found = True
    
    return issues_found

def main():
    mods_dir = 'mods'
    
    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            print(f"Checking {file_path}...")
            
            try:
                with open(file_path, 'r') as file:
                    data = toml.load(file)
                
                # Run all checks
                issues = check_for_missing_keys(file_path, data)
                if not issues: # Only check for URL malformation if basic keys are present
                    check_for_malformed_url(file_path, data)

            except toml.TomlDecodeError as e:
                print(f"Error parsing TOML in {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path}: {e}")
            
    print("Finished checking all files.")

if __name__ == "__main__":
    main()