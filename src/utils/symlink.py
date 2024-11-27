import os

def create_symlinks(source_dir:str, target_dir:str, exclude_dir:str, target_dir_prefix:str=""):
    current_path = os.path.dirname(os.path.realpath(__file__)).replace('utils','').removesuffix('/').replace('src', '').removesuffix('/')
    target_path = os.path.join(current_path, target_dir, target_dir_prefix)
    source_path = os.path.join(current_path, source_dir)

    # Ensure target_dir exists
    os.makedirs(target_path, exist_ok=True)
    print(f"Target directory created: {target_path}")

    # Iterate all directories in source_dir
    for folder_name in os.listdir(source_path):
        folder_path = os.path.join(source_path, folder_name)

        # Skip excluded directories
        if os.path.isdir(folder_path) and folder_name != exclude_dir:
            symlink_target = os.path.join(target_path, folder_name)
            print(f"Creating symlink: {folder_path} -> {symlink_target}")

            # Remove existing symlink or directory
            if os.path.exists(symlink_target):
                print(f"Removing existing symlink or file: {symlink_target}")
                os.remove(symlink_target)

            # Create symlink
            os.symlink(folder_path, symlink_target)
            print(f"Created symlink: {folder_name} -> {symlink_target}")

