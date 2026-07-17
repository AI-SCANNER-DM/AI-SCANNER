"""
File Manager Module

Handles all file and folder operations
for the AI Digitalised Document Scanner.
"""

import os
import shutil


def create_folder(folder_path):
    """
    Create a folder if it does not exist.
    """
    os.makedirs(folder_path, exist_ok=True)


def save_text(file_path, text):
    """
    Save OCR text into a text file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def read_text(file_path):
    """
    Read text from a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def copy_file(source, destination):
    """
    Copy a file.
    """
    shutil.copy(source, destination)


def move_file(source, destination):
    """
    Move a file.
    """
    shutil.move(source, destination)


def delete_file(file_path):
    """
    Delete a file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def rename_file(old_name, new_name):
    """
    Rename a file.
    """
    if os.path.exists(old_name):
        os.rename(old_name, new_name)


def file_exists(file_path):
    """
    Check whether a file exists.
    """
    return os.path.exists(file_path)


def list_files(folder_path):
    """
    Return all files inside a folder.
    """
    if not os.path.exists(folder_path):
        return []

    return os.listdir(folder_path)