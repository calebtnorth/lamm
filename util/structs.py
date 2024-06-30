# LANMM Structures
# Custom data structures to make managing data easier

from os import path

# Simple data structure for upload information
class UploadStats:
    def __init__(self, file_count:int, size_b:int):
        self.file_count = file_count
        self.size_b = size_b