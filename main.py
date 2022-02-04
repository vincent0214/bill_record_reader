import os
import pandas as pd


def make_target_dir():
    if not os.path.exists("./target"):
        os.mkdir("./target")

def make_temp_dir():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

def scan_file(path):
    files = []

    def _scan_file(path):
        for i in os.listdir(path):
            file_path = path + "/" + i
            if os.path.isdir(file_path):
                _scan_file(file_path)
            else:
                files.append(file_path)

    _scan_file(path)
    return files


def get_tables(files):
    tables = []
    for file in files:
        if file.endswith("xlsx"):
            table = pd.read_excel(file)
            tables.append(table)
    return tables


def merge(tables):
    result = None
    for table in tables:
        if result is None:
            result = table
        result = result.append(table, ignore_index=True)
    result.reset_index(drop=True)
    return result

make_target_dir()
files = scan_file(r"./temp/")
tables = get_tables(files)
result = merge(tables)
result.to_excel("./target/2021-收支表.xlsx", index=False, sheet_name="收支")
