from re import T
from numpy import column_stack
import pandas as pd


class AlipayRecordReader:
    def __init__(self, file):
        self.file = file

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
            return pd.read_excel(path, encoding="GBK")
        else:
            print("无法识别文件类型")
            return None

    def remove_rows(self, table):
        """
        删除多余的记录
        """
        remove_index = table.loc[table["收/支"] == "其他"].index  # 删除收/支为"其他"的记录
        return table.drop(index=remove_index)  # 按条件删除数据

    def save_file(self, output_path="./ww.xlsx"):
        table = self.get_table(self.file)
        table.drop(columns=["Unnamed: 11"], inplace=True)  # 删除列
        table.dropna(subset=["交易时间"], inplace=True)  # 删除交易时间为空的数据
        table = self.remove_rows(table)
        table.sort_values("交易时间", inplace=True)

        table.to_excel(output_path, index=False)


reader = AlipayRecordReader("./alipay_record_20220202_204423.csv")
reader.save_file(output_path="./2021年支付宝收支表.xlsx")
