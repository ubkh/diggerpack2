import os
import toml

def get_base_filename(filename):
    """
    Strips the '.pw.toml' extension and returns the base filename.
    """
    if filename.endswith('.pw.toml'):
        return filename[:-len('.pw.toml')]
    return filename

def main():
    """
    Main function to orchestrate the process.
    """
    mods_dir = 'mods'
    client_patch_file = 'client_patch.txt'
    server_blacklist_file = 'server_blacklist.txt'

    if not os.path.exists(mods_dir):
        print(f"Error: The directory '{mods_dir}' does not exist.")
        return

    # Load mod names to be patched or blacklisted into sets for quick lookup
    client_mods_to_patch = set()
    server_mods_to_blacklist = set()

    if os.path.exists(client_patch_file):
        with open(client_patch_file, 'r') as f:
            for line in f:
                mod_name = line.strip()
                if mod_name:
                    client_mods_to_patch.add(mod_name)
    else:
        print(f"Warning: The file '{client_patch_file}' does not exist. Skipping client patch.")

    if os.path.exists(server_blacklist_file):
        with open(server_blacklist_file, 'r') as f:
            for line in f:
                mod_name = line.strip()
                if mod_name:
                    server_mods_to_blacklist.add(mod_name)
    else:
        print(f"Warning: The file '{server_blacklist_file}' does not exist. Skipping server blacklist.")
    
    print("\nStarting mod side update process...")
    
    # Iterate through each .pw.toml file only once
    for filename in os.listdir(mods_dir):
        if filename.endswith('.pw.toml'):
            file_path = os.path.join(mods_dir, filename)
            
            try:
                with open(file_path, 'r') as f:
                    data = toml.load(f)

                # Use the filename as the unique identifier
                mod_filename_in_file = get_base_filename(filename)
                current_side = data.get('side')
                updated = False

                # Check if the mod is in the client patch list
                if mod_filename_in_file in client_mods_to_patch:
                    if current_side != 'both':
                        data['side'] = 'both'
                        updated = True
                        print(f"Updated '{mod_filename_in_file}' to side='both' in {file_path}")
                    client_mods_to_patch.remove(mod_filename_in_file)

                # Check if the mod is in the server blacklist
                if mod_filename_in_file in server_mods_to_blacklist:
                    if current_side != 'client':
                        data['side'] = 'client'
                        updated = True
                        print(f"Updated '{mod_filename_in_file}' to side='client' in {file_path}")
                    server_mods_to_blacklist.remove(mod_filename_in_file)

                if updated:
                    with open(file_path, 'w') as f:
                        toml.dump(data, f)
            
            except toml.TomlDecodeError as e:
                print(f"Error parsing TOML in {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path}: {e}")
    
    print("\nFinished mod side update process.")
    
    # Report any unhandled mods
    if client_mods_to_patch:
        print("\nWarning: The following mods were not found for client patching:")
        for name in client_mods_to_patch:
            print(f"- {name}")
            
    if server_mods_to_blacklist:
        print("\nWarning: The following mods were not found for server blacklisting:")
        for name in server_mods_to_blacklist:
            print(f"- {name}")

if __name__ == "__main__":
    main()