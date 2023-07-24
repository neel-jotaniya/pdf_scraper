import os

# Set the path to the folder you want to count the files in
folder_path = './PDFS'

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Count the number of files in the folder
num_files = len(files)

# Print the result
print(f"There are {num_files} files in {folder_path}")
