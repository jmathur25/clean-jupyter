# clean-jupyter
Script that lets you reorder the cells in a Jupyter notebook without re-running the code. You can clean an entire folder and its subfolders, and remove error messages.

# Quick Start
Run:
`python clean.py <PATH_TO_FILE_OR_FOLDER>`

It will automatically detect if the target is a file or a folder. If it is a folder, it will modify every .ipynb files.

# How it works
The script simply opens up the .ipynb file, which can be read as a JSON object, and changes the numbering in the cells.
