import os
import shutil
import random

src_folder = "images/"
# dst_folder = "/path/to/dst/folder"

# get all folders in /images
folders = os.listdir(src_folder)


for folder in folders:
    folder = os.path.join(src_folder, folder)
    dst_folder = os.path.join(src_folder + "_test")

    print("Moving files from " + folder + " to " + dst_folder)
    # Make sure the destination folder exists
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # List all files in the source folder
    files = os.listdir(folder)

    # Shuffle the list of files
    random.shuffle(files)

    # Calculate how many files to move
    num_files_to_move = len(files) // 3

    # Move the files to the destination folder
    for i in range(num_files_to_move):
        file = files[i]
        src_path = os.path.join(folder, file)
        dst_path = os.path.join(dst_folder, file)
        shutil.move(folder, dst_path)
