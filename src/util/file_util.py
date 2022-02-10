import shutil
import os
import sys


class FileUtil:
    @staticmethod
    def scan_file(path):
        """
        扫描文件夹下的所有文件
        """
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

    @staticmethod
    def clean_dir(path):
        """
        清空文件夹
        """
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    @staticmethod
    def get_class_file_path(clazz):
        """
        获取类文件所在路径
        clazz: 类
        """
        path = os.path.abspath(sys.modules[clazz.__module__].__file__)
        return path

    @staticmethod
    def get_class_file_dir_path(clazz):
        """
        获取类文件所在目录路径
        clazz: 类
        """
        path = os.path.abspath(sys.modules[clazz.__module__].__file__)
        return os.path.dirname(path)

    @staticmethod
    def get_father_path(path):
        """
        获取上级路径
        """
        return os.path.abspath(os.path.join(path, ".."))

    @staticmethod
    def get_project_root_path():
        """
        获取项目根路径
        """
        path = FileUtil.get_class_file_dir_path(FileUtil)
        return os.path.abspath(os.path.join(path, "../../"))

    @staticmethod
    def get_source_dir_path():
        """
        获取source目录路径
        """
        return File(FileUtil.get_source_dir_path())

    @staticmethod
    def get_temp_dir_path():
        """
        获取temp目录路径
        """
        return File(FileUtil.get_temp_dir_path())

    @staticmethod
    def get_target_dir_path():
        """
        获取target目录路径
        """
        return File(FileUtil.get_target_dir_path())


class File:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = os.path.abspath(path)
