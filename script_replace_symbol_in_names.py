import os

def replace_symbol_in_names(directory, target_symbol, replacement_symbol):
    for root, dirs, files in os.walk(directory, topdown=False):
        # Rename files
        for filename in files:
            if target_symbol in filename:  # Replace target symbol in file name
                new_filename = filename.replace(target_symbol, replacement_symbol)
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed file: {old_path} -> {new_path}")

        # Rename directories
        for dirname in dirs:
            if target_symbol in dirname:  # Replace target symbol in directory name
                new_dirname = dirname.replace(target_symbol, replacement_symbol)
                old_path = os.path.join(root, dirname)
                new_path = os.path.join(root, new_dirname)
                os.rename(old_path, new_path)
                print(f"Renamed directory: {old_path} -> {new_path}")

# Example usage
# Replace 'your_directory_path_here' with the path to the folder you want to process
folder_path = "csv/2024-11-24"
target = ":"  # Symbol to replace
replacement = "_"  # Replacement symbol

replace_symbol_in_names(folder_path, target, replacement)
