import os
import toml

def fix_url_encoding(file_path):
    """
    Reads a TOML file, fixes the URL encoding, and writes the changes back.
    """
    try:
        with open(file_path, 'r') as f:
            data = toml.load(f)

        if 'download' in data and 'url' in data['download']:
            original_url = data['download']['url']
            
            # Use string replace to fix only the specific characters that cause issues
            corrected_url = original_url.replace(' ', '%20').replace('[', '%5B').replace(']', '%5D')
            
            # Check for changes before writing to avoid unnecessary file writes
            if original_url != corrected_url:
                data['download']['url'] = corrected_url
                
                with open(file_path, 'w') as f:
                    toml.dump(data, f)
                print(f"Fixed URL encoding in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    mods_dir = 'mods'
    
    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            fix_url_encoding(file_path)

    print("Finished checking and fixing URLs in all .pw.toml files.")

if __name__ == "__main__":
    main()