import os

class Folder:
    def __init__(self, path_to_folder) -> None:
        self.path_to_folder: str = path_to_folder
        self.root: str = path_to_folder[len(os.getcwd()):]

    def __repr__(self) -> str:
        return self.root