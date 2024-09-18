import tkinter as tk
from tkinter import filedialog
import unreal
import os

def select_folder():
    # Create a root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a dialog to select a folder
    folder_path = filedialog.askdirectory()

    if folder_path:
        unreal.log(f"Selected folder: {folder_path}")
        return folder_path
    else:
        unreal.log_warning("No folder selected.")
        return None

def list_files_in_folder(folder_path):
    # check if the folder path is valid
    if not folder_path or not os.path.isdir(folder_path):
        unreal.log_error(f"Invalid folder path: {folder_path}")
        return []

    # get all files in the folder
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append(file)

    multiline_string = "\n".join(file_list)
    return multiline_string

def display_files_in_textbox(file_list, textbox):
    # list all files in the folder
    content = "\n".join(file_list)
    textbox.set_text(content)
    unreal.log(f"Displayed {len(file_list)} files in the textbox.")

def list_assets_in_folder(assets):
    multiline_string = '\n'.join(assets)
    return multiline_string