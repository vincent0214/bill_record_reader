from re import I
import pandas as pd
from util.file_util import FileUtil
from util.pandas_util import PandasUtil


class AlipayRecordReader:
    def __init__(self, files):
        self.files = files

    def get_table(self, path):
        """
        读取表格
        path: 文件路径
        """
        if path.endswith(".csv"):
            return pd.read_csv(
                path, encoding="GBK", header=1, sep="\s*,\s*"
            )  # sep="\s*,\s*"去除csv空格
        elif path.endswith(".xlsx"):
            return pd.read_excel(path, header=1)
        else:
            print("无法识别文件类型")
            return None

    def remove_rows(self, table):
        """
        删除多余的记录(删除行)
        """
        # 删除收/支为"其他"的记录
        remove_index = table.loc[table["收/支"] == "其他"].index
        table.drop(index=remove_index, inplace=True)  # 按条件删除数据
        # 删除交易关闭(无效)的支出记录
        remove_index = table[(table["收/支"] == "支出") & (table["交易状态"] == "交易关闭")].index
        table.drop(index=remove_index, inplace=True)  # 按条件删除数据
        # 删除交易时间为空的数据
        table.dropna(subset=["交易时间"], inplace=True)

    def remove_columns(self, table):
        """
        删除列
        """
        cols = ["交易订单号", "商家订单号", "对方账号"]
        if "Unnamed: 11" in table.columns:
            cols.append("Unnamed: 11")
        table.drop(columns=cols, inplace=True)
        return table

    def get_table_by_files(self, files):
        tables = []
        for file in files:
            result = self.get_table(file.path)
            tables.append(result)
        return PandasUtil.merge_tables(tables)

    def save_file(self, filename="ww.xlsx"):
        table = self.get_table_by_files(self.files)
        self.remove_rows(table)
        self.remove_columns(table)
        table.sort_values("交易时间", inplace=True)
        table["来源"] = "支付宝"

        output_path = r"./temp/" + filename
        table.to_excel(output_path, index=False)


def scan_file_alipay_csv(path="./source"):
    """
    扫描支付宝csv文件
    """
    result = []
    files = FileUtil.scan_file(path)
    for file in files:
        file_name = file.name
        if file_name.endswith(".csv") and file_name.startswith("alipay_record"):
            result.append(file)
    return result


def read_alipay_record():
    files = scan_file_alipay_csv("./source")
    reader = AlipayRecordReader(files)
    reader.save_file(filename="支付宝收支表.xlsx")
