# LANMM Argument Utility
# Read command line input and provide configuration
# information for app.py and other modules

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
            with open(".upload", "r+") as file:
                Arg.upload_path = file.read()
        except FileNotFoundError:
            print("[-] Create the .upload file first")
            quit()