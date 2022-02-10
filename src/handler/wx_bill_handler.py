import sys

sys.path.append("..")

import pandas as pd
from util.pandas_util import PandasUtil
from util.file_util import FileUtil
from handler.base_handler import BaseHandler


class WxBillHandler(BaseHandler):
    def __init__(self):
        self.files = []
        self.table = None

    def handle(self):
        self.__scan_csv_files()
        self.__calculate_table()
        self.__save_file()

    def __scan_csv_files(self):
        """
        扫描微信CSV文件
        """
        result = []
        files = FileUtil.scan_file(super().get_source_dir().path)
        for file in files:
            file_name = file.name
            if file_name.endswith(".csv") and file_name.startswith("微信支付账单"):
                result.append(file)
        self.files = result

    def __calculate_table(self):
        result1 = self.__read_pay()
        result2 = self.__read_income()
        self.table = result1.append(result2, ignore_index=True).reset_index(drop=True)

        self.table = self.__alipay_format(self.table)
        self.table["金额"] = self.table["金额"].apply(lambda x: x.replace("¥", ""))
        self.table["来源"] = "微信"

    def __read_pay(self):
        """
        读取支出
        """
        tables = []
        for file in self.files:
            table = self.__read(file.path, "支出")
            tables.append(table)
        result = PandasUtil.merge_tables(tables)
        return result

    def __read_income(self):
        """
        读取收入
        """
        tables = []
        for file in self.files:
            table = self.__read(file.path, "收入")
            tables.append(table)
        result = PandasUtil.merge_tables(tables)
        return result

    def __read(self, path, type):
        """
        path: 路径
        type: 收/支类型
        """
        table = pd.read_csv(path, header=16)  # 从17行开始读取, header=0为第1行
        return table.loc[table["收/支"].apply(lambda x: x == type)]

    def __alipay_format(self, table):
        """
        微信excel格式转支付宝excel格式
        """
        PandasUtil.change_col_place(table, "收/支", 0, "收/支")
        PandasUtil.change_col_place(table, "交易对方", 1, "交易对方")
        PandasUtil.change_col_place(table, "商品", 2, "商品说明")
        PandasUtil.change_col_place(table, "支付方式", 3, "收/付款方式")
        PandasUtil.change_col_place(table, "金额(元)", 4, "金额")
        PandasUtil.change_col_place(table, "当前状态", 5, "交易状态")
        PandasUtil.change_col_place(table, "交易类型", 6, "交易分类")
        PandasUtil.change_col_place(table, "交易时间", 7, "交易时间")
        table.drop(columns=["备注", "交易单号", "商户单号"], inplace=True)
        return table

    def __save_file(self, filename="微信收支表.xlsx"):
        self.table.to_excel(super().get_temp_dir().path + "/" + filename, index=False, sheet_name="收支")

