# LANMM Utilities
# Various helper classes for LANMM

from os import remove, listdir, stat, path
from util.structs import UploadStats

# A class of static methods designed to handle
# adding, deleting and managing audio files
class FileUtil:

    upload_path:str = ""
    
    # Delete the requested file and return a boolean
    # status to indicate success or failure
    @staticmethod
    def delete_upload(filename:str) -> bool:
        try:
            remove(
                path.join(FileUtil.upload_path, filename)
            )
            return True
        except Exception as e:
            print(f"[-] An error occured trying to delete file {filename}\n{e}")
        return False

    # Empty the upload folder
    @staticmethod
    def delete_upload_folder():
        for upload in listdir(FileUtil.upload_path):
            FileUtil.delete_upload(upload)

    # Return the number of files and cumulative size of
    # all uploads in bytes in the uploads directory
    @staticmethod
    def get_upload_stats() -> UploadStats:
        # Sum total bytes
        size_b:int = 0
        for file in list(FileUtil.upload_path):
            size_b += stat(path.join(FileUtil.upload_path, file)).st_size

        return UploadStats(
            len(listdir(FileUtil.upload_path)), # Count
            size_b,                             # Size
        )

    # Grab all files under the uploads folder and return a list of filenames
    def dump_uploads() -> list[str]:
        files:list[str] = []
        for file in listdir(FileUtil.upload_path):
            files.append(file)
        return files