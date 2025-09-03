import os
import toml

## Updated Check for Malformed URLs

def check_for_malformed_url(file_path, data):
    """
    Checks if a download URL is malformed due to unencoded characters.
    """
    # Check for the presence of download and url keys before attempting to access them
    if not ('download' in data and 'url' in data['download']):
        return False
        
    url = data['download']['url']
    issues_found = False

    # Check for specific unencoded characters that should be percent-encoded
    if ' ' in url:
        print(f"Warning: Malformed URL in {file_path}. Reason: Contains unencoded spaces.")
        issues_found = True
    if '[' in url:
        print(f"Warning: Malformed URL in {file_path}. Reason: Contains unencoded '['.")
        issues_found = True
    if ']' in url:
        print(f"Warning: Malformed URL in {file_path}. Reason: Contains unencoded ']'.")
        issues_found = True

    return issues_found

## Check for Missing Keys

def check_for_missing_keys(file_path, data):
    """
    Checks a .pw.toml file for missing required keys.
    """
    issues_found = False
    
    # Check for the download section first, as it's the root of your previous errors
    if 'download' not in data:
        print(f"Error: Missing section '[download]' in {file_path}")
        issues_found = True
    elif 'url' not in data['download']:
        print(f"Error: Missing key 'url' in section '[download]' in {file_path}")
        issues_found = True

    return issues_found

## Main Logic

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
                if not issues:
                    check_for_malformed_url(file_path, data)

            except toml.TomlDecodeError as e:
                print(f"Error parsing TOML in {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path}: {e}")
            
    print("Finished checking all files.")

if __name__ == "__main__":
    main()