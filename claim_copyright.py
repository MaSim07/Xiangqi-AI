"""
Copyright (C) 2021-2022 Simon Ma <https://github.com/Simuschlatz> 
- All Rights Reserved. You may use, distribute and modify this code
under the terms of the GNU General Public License
"""
import os
copyright_text = '''"""
Copyright (C) 2021-2022 Simon Ma <https://github.com/Simuschlatz> 
- All Rights Reserved. You may use, distribute and modify this code
under the terms of the GNU General Public License
"""
'''
msg_lines = len(copyright_text.split("\n"))

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, _, files in os.walk(directory):
        for file in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, file)
            if file.endswith(".py") and not file.endswith("__init__.py"):
                file_paths.append(filepath)  # Add it to the list.

    return file_paths
def write_copyright_msg():
    for filepath in all_file_paths:
        with open(filepath, "r+") as f:
            contents = f.read()
            file_lines = "\n".join(contents.split("\n")[:msg_lines-1]) + "\n"
            print(file_lines)
            print(copyright_text)
            if file_lines == copyright_text:
                print("YEHAA")
                continue
            f.seek(0)
            f.write(copyright_text + contents)

def delete_copyright_msg():
    for filepath in all_file_paths:
        with open(filepath, "r") as f:
            contents = f.readlines()
            file_lines = "".join(contents[:msg_lines-1])
            print(file_lines)
            print(copyright_text)
            if file_lines != copyright_text:
                continue
        with open(filepath, "w") as f:
            f.seek(0)
            f.write("".join(contents[msg_lines-1:]))

# All files in working tree, except for __init__ files
all_file_paths = get_filepaths(".")
# this_file = os.path.abspath(__file__)
write_copyright_msg()
# delete_copyright_msg()
