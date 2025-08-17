import os
import subprocess
import shutil
import time
import argparse
import platform
import sys


def get_file_list(directory):
    """
    Returns a list of file names (with full path) in the specified directory.
    
    :param directory: The directory to scan for files.
    :return: A list of full paths to files within the directory.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            if not os.path.islink(file_path):  # Exclude symbolic links
                file_list.append(file_path)
    return file_list

def copy_missing_files(src_directory, target_directory):
    """
    Copies missing files from the source directory to the target directory.
    
    :param src_directory: The source directory containing files to be copied.
    :param target_directory: The destination directory where files will be copied.
    """
    # Get list of files in both directories
    src_files = set(get_file_list(src_directory))
    target_files = set(get_file_list(target_directory))

    missing_files = src_files - target_files

    for file_path in missing_files:
        relative_path = os.path.relpath(file_path, start=src_directory)
        dest_path = os.path.join(target_directory, relative_path)

        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Copy the file to target path
        shutil.copy2(file_path, dest_path)  # Using copy2 preserves metadata

if __name__ == "__main__":
    source_dir = r"./n8n_workflows"
    target_dir = r"./n8n/demo-data/workflows"

    print("Copying missing files from", source_dir, "to", target_dir)
    
    # Perform the file copying operation
    copy_missing_files(source_dir, target_dir)