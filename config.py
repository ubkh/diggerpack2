import os

# --- Path and Directory Configuration ---

# The root directory for copying files from, typically the `minecraft` folder of your instance.
# The `os.path.expanduser` function handles the '~' character correctly.
ROOT_COPY_PATH = os.path.expanduser("~/Library/Application Support/PrismLauncher/instances/dp2/minecraft")

# A list of additional directories and files to copy from the ROOT_COPY_PATH.
# These will be copied to the `MODS_DIR` folder.
ADDITIONAL_COPY_PATHS = [
    "config",
]

# The name of the directory containing the .pw.toml files relative to the ROOT_COPY_PATH.
SOURCE_MODS_DIR_NAME = "mods/.index"

# The directory where the final .pw.toml files will be placed for packwiz.
MODS_DIR = "mods"

# The directory containing any additional files to be copied, like custom mods.
UNKNOWN_MODS_DIR = "unknown-mods"

# The text files used to update the 'side' key for mods.
CLIENT_PATCH_FILE = "client_patch.txt"
SERVER_BLACKLIST_FILE = "server_blacklist.txt"

# The name of the signature file.
SIG_FILE = "unsup.sig"

# The location of the signify secret key used for signing.
SIGNIFY_SECRET_KEY = "sig/dp2.sec"

# The main packwiz configuration file to be signed.
PACKWIZ_CONFIG_FILE = "pack.toml"

# --- Scripts to run ---
# A list of the python scripts to be run in order.
SCRIPTS = [
    "strip_toml.py",
    "fix_urls.py",
    "update_side.py",
    "check_mods.py"
]