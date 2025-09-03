# This file is part of Diggerpack 2. Copyright (C) 2025 Ubayd Khan

import os
import shutil
import subprocess
import hashlib
import toml
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

def generate_toml_for_unknown_mods():
    """
    Creates .pw.toml files for unknown mods and copies them to the mods directory.
    """
    print(f"\n--- Processing unknown mods in '{UNKNOWN_MODS_DIR}' ---")
    
    if not os.path.exists(UNKNOWN_MODS_DIR):
        print(f"Warning: Directory '{UNKNOWN_MODS_DIR}' not found. Skipping unknown mods.")
        return

    for mod_data in UNKNOWN_MODS_TOML_DATA:
        filename = mod_data.get('filename')
        name = mod_data.get('name')
        side = mod_data.get('side', 'both')
        
        if not filename or not name:
            print(f"Error: Skipping unknown mod with incomplete data: {mod_data}")
            continue

        mod_jar_path = os.path.join(UNKNOWN_MODS_DIR, filename)
        if not os.path.exists(mod_jar_path):
            print(f"Warning: JAR file '{filename}' not found in '{UNKNOWN_MODS_DIR}'. Skipping.")
            continue

        # Calculate SHA256 hash of the JAR file
        sha256_hash = hashlib.sha256()
        with open(mod_jar_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        # Construct the TOML content
        toml_content = {
            "name": name,
            "filename": filename,
            "side": side,
            "download": {
                "url": f"{UNKNOWN_MODS_URL_BASE}{filename}",
                "hash": sha256_hash.hexdigest(),
                "hash-format": "sha256",
                "mode": "url"
            }
        }
        
        # Write the TOML content to a new file in the mods directory
        toml_filename = f"{os.path.splitext(filename)[0]}.pw.toml"
        toml_path = os.path.join(MODS_DIR, toml_filename)
        
        with open(toml_path, "w") as toml_file:
            toml.dump(toml_content, toml_file)
        
        print(f"Created TOML file for '{filename}' at '{toml_path}'.")

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

    # --- Process unknown mods ---
    generate_toml_for_unknown_mods()
    
    # --- Step 2: Run Scripts ---
    print(f"\n--- Step 2: Running scripts ---")

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