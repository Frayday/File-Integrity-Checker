import hashlib
import os
import time
import json

def generate_hash(filepath, algorithm='sha256'):
    """Generates a hash for a given file."""
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as file:
            while True:
                chunk = file.read(4096)  # Read in chunks to handle large files
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None  # Handle cases where the file doesn't exist

def store_hashes(filepaths, hash_file="file_hashes.json", algorithm='sha256'):
    """Generates and stores hashes for multiple files in a JSON file."""
    hashes = {}
    for filepath in filepaths:
        file_hash = generate_hash(filepath, algorithm)
        if file_hash:  # Only store hashes if the file exists
            hashes[filepath] = file_hash

    try:  # Use a try-except block for file operations
        with open(hash_file, 'w') as f:
            json.dump(hashes, f, indent=4)
    except (IOError, OSError) as e:
        print(f"Error writing to hash file: {e}")
    return hashes



def check_integrity(hash_file="file_hashes.json", algorithm='sha256'):
    """Checks the integrity of files against stored hashes."""
    try:
         with open(hash_file, 'r') as f:
            stored_hashes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading hash file or file does not exist: {e}")  # Clearer error message
        return


    modified_files = []
    for filepath, stored_hash in stored_hashes.items():
        current_hash = generate_hash(filepath, algorithm)
        if current_hash is None:  # File has been deleted
            modified_files.append((filepath, "DELETED"))
        elif current_hash != stored_hash:
            modified_files.append((filepath, "MODIFIED"))
    return modified_files

def alert_user(modified_files):
    """Alerts the user about modified files."""
    if modified_files:
        print("File Integrity Check Alert:")
        for filepath, status in modified_files:
            print(f"- {filepath}: {status}")
    else:
        print("All files intact.")


def monitor_files(filepaths, interval=60, hash_file="file_hashes.json", algorithm='sha256'):
    """Monitors files for changes at a specified interval."""


    initial_hashes = store_hashes(filepaths, hash_file, algorithm)  # Store initial hashes first

    while True:
        modified_files = check_integrity(hash_file, algorithm)
        alert_user(modified_files)
        time.sleep(interval)  # Check every 'interval' seconds





if __name__ == "__main__":
    files_to_monitor = [
        "HW.txt",  # Replace with the files you want to monitor
        "important_file2.py",
        "sensitive_data.csv",
    ]

    monitor_files(files_to_monitor, interval=30) # Check every 30 seconds