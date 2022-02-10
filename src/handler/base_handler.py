import os
import sys

sys.path.append("..")
from util.file_util import File, FileUtil


class BaseHandler:

    def get_source_dir(self):
        return File(FileUtil.get_project_root_path() + os.path.sep + "source")

    def get_temp_dir(self):
        return File(FileUtil.get_project_root_path() + os.path.sep + "temp")

    def get_target_dir(self):
        return File(FileUtil.get_project_root_path() + os.path.sep + "target")
