import imp
import os
import pandas as pd
from util.file_util import FileUtil
from util.pandas_util import PandasUtil
from alipay_record_reader import read_alipay_record
from wx_record_reader import read_wx_record
import shutil

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

shutil.rmtree("./temp")
make_temp_dir()
read_alipay_record()
read_wx_record()
files = FileUtil.scan_file(r"./temp")
tables = get_tables(files)
result = PandasUtil.merge_tables(tables)
result.to_excel("./target/2021-收支表.xlsx", index=False, sheet_name="收支")
