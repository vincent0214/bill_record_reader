import os
import pandas as pd
from util.file_util import FileUtil
from util.pandas_util import PandasUtil
from alipay_record_reader import read_alipay_record
from wx_record_reader import read_wx_record


def make_target_dir():
    if not os.path.exists("./target"):
        os.mkdir("./target")


def make_temp_dir():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")


def get_tables(files):
    tables = []
    for file in files:
        if file.name.endswith("xlsx"):
            table = pd.read_excel(file.path)
            tables.append(table)
    return tables


def main(output_file_name):
    temp_dir_path = os.getcwd() + "/temp"
    FileUtil.clean_dir(temp_dir_path)
    FileUtil.clean_dir("./target")
    read_alipay_record()
    read_wx_record()
    files = FileUtil.scan_file(temp_dir_path)
    tables = get_tables(files)
    result = PandasUtil.merge_tables(tables)
    result.to_excel(f"./target/{output_file_name}", index=False, sheet_name="收支")


output_file_name = "2021年收支表.xlsx"
main(output_file_name)
