import sys

sys.path.append("..")

import pandas as pd
from util.file_util import FileUtil
from util.pandas_util import PandasUtil
from handler.base_handler import BaseHandler


class AlipayBillHandler(BaseHandler):
    def __init__(self):
        self.files = []
        self.table = None

    def handle(self):
        self.__scan_csv_files()
        self.__calculate_table()
        self.__save_file()

    def __scan_csv_files(self):
        """
        扫描支付宝csv文件
        """
        result = []
        files = FileUtil.scan_file(super().get_source_dir().path)
        for file in files:
            file_name = file.name
            if file_name.endswith(".csv") and file_name.startswith("alipay_record"):
                result.append(file)
        self.files = result

    def __calculate_table(self):
        table = self.__get_table_by_files(self.files)
        self.__remove_rows(table)
        self.__remove_columns(table)
        table.sort_values("交易时间", inplace=True)
        table["来源"] = "支付宝"
        self.table = table

    def __remove_rows(self, table):
        """
        删除多余的记录(删除行)
        """
        # 删除收/支为"其他"的记录
        remove_index = table.loc[table["收/支"] == "其他"].index
        table.drop(index=remove_index, inplace=True)
        # 删除交易关闭(无效)的支出记录
        remove_index = table[(table["收/支"] == "支出") & (table["交易状态"] == "交易关闭")].index
        table.drop(index=remove_index, inplace=True)
        # 删除交易时间为空的数据
        table.dropna(subset=["交易时间"], inplace=True)

    def __remove_columns(self, table):
        """
        删除列
        """
        cols = ["交易订单号", "商家订单号", "对方账号"]
        if "Unnamed: 11" in table.columns:
            cols.append("Unnamed: 11")
        table.drop(columns=cols, inplace=True)
        return table

    def __get_table_by_files(self, files):
        tables = []
        for file in files:
            result = pd.read_csv(
                file.path, encoding="GBK", header=1, sep="\s*,\s*"
            )  # sep="\s*,\s*"去除csv空格
            tables.append(result)
        return PandasUtil.merge_tables(tables)

    def __save_file(self, filename="支付宝收支表.xlsx"):
        output_path = super().get_temp_dir().path + "/" + filename
        self.table.to_excel(output_path, index=False)

