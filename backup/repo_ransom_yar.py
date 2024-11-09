# https://github.com/advanced-threat-research/Yara-Rules

import os
import shutil
from tkinter import filedialog
from tkinter import Tk

def organize_folders(root_folder):
    print("Organizing folders in:", root_folder)
    # Get all files recursively in the root folder
    files = []
    for root, _, filenames in os.walk(root_folder):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    print("Files found:", files)
    
    # Create folders for each file extension and copy the parent folder structure
    for file in files:
        file_extension = file.split('.')[-1]
        file_directory = file.split('_')[1]
        file_directory = file_directory.split('.')[0]
        # print(file_extension)
        parent_folder = os.path.basename(os.path.dirname(file))
        new_folder_path = os.path.join(root_folder, file_extension, parent_folder, file_directory)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print("Created folder:", new_folder_path)

    # Move files to their respective folders
    for file in files:
        file_extension = file.split('.')[-1]
        file_directory = file.split('_')[1]
        file_directory = file_directory.split('.')[0]
        parent_folder = os.path.basename(os.path.dirname(file))
        new_path = os.path.join(root_folder, file_extension, parent_folder, file_directory, os.path.basename(file))
        print(new_path)
        shutil.move(file, new_path)
        print("Moved file:", os.path.basename(file), "to folder:", file_extension + '/' + parent_folder)

# Let the user select the malware-ioc folder
root = Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Select the malware-ioc folder")

# Organize the folders
if folder_path:
    organize_folders(folder_path)
    print("Folder structure organized successfully!")
else:
    print("No folder selected.")
