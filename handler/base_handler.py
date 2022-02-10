import sys

sys.path.append("..")
from util.file_util import File


class BaseHandler:
    def get_source_dir(self):
        return File("../source")

    def get_temp_dir(self):
        return File("../temp")
    
    def get_target_dir(self):
        return File("../target")
