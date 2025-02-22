import inspect
import os
import sys

# This file has utility functions for file handling


def relative_directory(*args):
    """Returns relative path of function args from where the func was called."""
    if hasattr(sys, "_MEIPASS"):
        # Running as PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        caller_frame = inspect.stack()[
            1
        ]  # Get the frame of the file that called this function a frame up the stack
        caller_file = (
            caller_frame.filename
        )  # Gets the file name of the file that called this function
        base_path = os.path.dirname(
            os.path.abspath(caller_file)
        )  # Get the directory of the file that called this function
    return os.path.join(base_path, *args)  # Join the base path with the args
