# LANMM Argument Utility
# Read command line input and provide configuration
# information for app.py and other modules

from os.path import join, abspath, dirname

class Arg:
    """
    Configuration variables

    - `Config.upload_path`   Filepath to audio file uploads
    """

    upload_path:str = ""

    @staticmethod
    def parse():
        global upload_path

        try:
            # Get the current path that the app file is in
            path = abspath(join(dirname(__file__), "../.upload"))

            with open(path, "r") as file:
                Arg.upload_path = file.read().strip()
        except FileNotFoundError:
            print("[-] Create the .upload file first")
            quit()