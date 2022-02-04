import imp


import os


class FileUtil:
    @staticmethod
    def scan_file(path):
        files = []

        def _scan_file(path):
            for file_name in os.listdir(path):
                file_path = path + "/" + file_name
                if os.path.isdir(file_path):
                    _scan_file(file_path)
                else:
                    file = File(file_path)
                    files.append(file)

        _scan_file(path)
        return files


class File:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = path
    
