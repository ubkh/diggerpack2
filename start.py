import os
import shutil
import subprocess
from config import *

def run_script(script_name):
    """A helper function to run other Python scripts."""
    print(f"\n--- Running {script_name} ---")
    try:
        # Use python3 to ensure the correct interpreter is used
        subprocess.run(["python3", script_name], check=True)
    except FileNotFoundError:
        print(f"Error: Python interpreter 'python3' or script '{script_name}' not found.")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        exit(1)

def copy_items(source_root, destination_root, items):
    """
    Copies a list of files or directories from a source root to a destination root.
    If a destination item exists, it is updated.
    """
    for item in items:
        source_path = os.path.join(source_root, item)
        dest_path = os.path.join(destination_root, item)
        
        if not os.path.exists(source_path):
            print(f"Warning: Source item '{source_path}' not found. Skipping.")
            continue
        
        if os.path.isdir(source_path):
            # Remove existing destination directory to ensure a clean copy
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
            print(f"Copied directory '{item}' to '{dest_path}'.")
        else:
            shutil.copy2(source_path, dest_path)
            print(f"Copied file '{item}' to '{dest_path}'.")

def main():
    """Main function to run the modpack construction pipeline."""
    
    # --- Step 1: Clear and Copy Files ---
    print(f"--- Step 1: Clearing existing {MODS_DIR} and copying files ---")
    
    # Clear existing mods folder
    if os.path.exists(MODS_DIR):
        print(f"Clearing existing {MODS_DIR} directory...")
        shutil.rmtree(MODS_DIR)
    os.makedirs(MODS_DIR)

    # Copy additional directories and files
    copy_items(ROOT_COPY_PATH, ".", ADDITIONAL_COPY_PATHS)

    # Copy .pw.toml files from the source mods location into the MODS_DIR
    source_mods_path = os.path.join(ROOT_COPY_PATH, SOURCE_MODS_DIR_NAME)
    print(f"Copying .pw.toml files from {source_mods_path}...")
    
    if not os.path.exists(source_mods_path):
        print(f"Error: Source mods directory '{source_mods_path}' not found.")
        exit(1)
    
    for filename in os.listdir(source_mods_path):
        if filename.endswith(".pw.toml"):
            source_path = os.path.join(source_mods_path, filename)
            dest_path = os.path.join(MODS_DIR, filename)
            shutil.copy2(source_path, dest_path)
    print(f"Copied .pw.toml files from {source_mods_path} to {MODS_DIR}.")

    # Copy files from unknown-mods
    copy_items(UNKNOWN_MODS_DIR, MODS_DIR, os.listdir(UNKNOWN_MODS_DIR) if os.path.exists(UNKNOWN_MODS_DIR) else [])
    
    # --- Step 2: Run Scripts ---
    for script in SCRIPTS:
        run_script(script)

    # --- Step 3: Run packwiz refresh ---
    print(f"\n--- Step 3: Running packwiz refresh ---")
    try:
        subprocess.run(["packwiz", "refresh"], check=True)
    except FileNotFoundError:
        print("Error: 'packwiz' command not found. Make sure it's in your PATH.")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running packwiz refresh: {e}")
        exit(1)

    # --- Step 4: Sign pack.toml ---
    print(f"\n--- Step 4: Signing {PACKWIZ_CONFIG_FILE} ---")
    # Remove existing unsup.sig file if it exists
    if os.path.exists(SIG_FILE):
        os.remove(SIG_FILE)
        print(f"Removed existing {SIG_FILE}.")

    # Run signify to create the new signature
    try:
        subprocess.run(["signify", "-S", "-s", SIGNIFY_SECRET_KEY, "-m", PACKWIZ_CONFIG_FILE, "-x", SIG_FILE], check=True)
    except FileNotFoundError:
        print("Error: 'signify' command not found. Make sure it's installed and in your PATH.")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running signify: {e}")
        exit(1)
    print(f"Successfully signed {PACKWIZ_CONFIG_FILE} and created {SIG_FILE}.")
    
    print("\n--- Modpack construction complete! ---")

if __name__ == "__main__":
    main()