import os

class IndexBuilder:

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))

        _filename, _file_ext = os.path.splitext(filepath)
        pass