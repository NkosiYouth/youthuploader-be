import os
import shutil

def delete_file_or_folder(path):
    try:
        # Check if the path exists
        if os.path.exists(path):
            # Check if it's a file
            if os.path.isfile(path):
                # Delete the file
                os.remove(path)
                print(f"File '{path}' deleted successfully.")
            else:
                # Delete the folder and all its content recursively
                shutil.rmtree(path)
                print(f"Folder '{path}' and its content deleted successfully.")
        else:
            print(f"Path '{path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting '{path}': {e}")
