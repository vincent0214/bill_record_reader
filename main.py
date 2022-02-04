import imp
import os
import pandas as pd
from util.FileUtil import FileUtil
from util.PandasUtil import PandasUtil


def make_target_dir():
    if not os.path.exists("./target"):
        os.mkdir("./target")


def make_temp_dir():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")


def get_tables(files):
    tables = []
    for file in files:
        if file.endswith("xlsx"):
            table = pd.read_excel(file)
            tables.append(table)
    return tables


make_target_dir()
files = FileUtil.scan_file(r"./temp/")
tables = get_tables(files)
result = PandasUtil.merge_tables(tables)
result.to_excel("./target/2021-收支表.xlsx", index=False, sheet_name="收支")
