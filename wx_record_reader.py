import pandas as pd
from util.pandas_util import PandasUtil
from util.file_util import FileUtil


class WxExcelReader:
    def __init__(self, files=[]):
        self.files = files

    def get_table(self, path):
        """
        读取表格
        path: 文件路径
        """
        if path.endswith(".csv"):
            return pd.read_csv(path, header=16)  # 从17行开始读取, header=0为第1行
        elif path.endswith(".xlsx"):
            return pd.read_excel(path, header=16)  # 从17行开始读取, header=0为第1行
        else:
            print("无法识别文件类型")
            return None

    def read(self, path, type):
        """
        path: 路径
        type: 收/支类型
        """
        table = self.get_table(path)
        return table.loc[table["收/支"].apply(lambda x: x == type)]

    def read_pay(self):
        """
        读取支出
        """
        tables = []
        for file in self.files:
            table = self.read(file.path, "支出")
            tables.append(table)
        result = PandasUtil.merge_tables(tables)
        return result

    def read_income(self):
        """
        读取收入
        """
        tables = []
        for file in self.files:
            table = self.read(file.path, "收入")
            tables.append(table)
        result = PandasUtil.merge_tables(tables)
        return result

    def alipay_format(self, table):
        """
        微信excel格式转支付宝excel格式
        """

        def change_col_place(table, name, new_place, new_name=None):
            """
            移动列
            table: 表格
            name: 原列名
            new_plack: 新位置
            new_name: 新列名
            """
            val = table[name]
            table.drop(labels=[name], axis=1, inplace=True)
            if new_name is None:
                table.insert(new_place, column=name, value=val)  # 插入列
            else:
                table.insert(new_place, column=new_name, value=val)  # 插入列

        change_col_place(table, "收/支", 0, "收/支")
        change_col_place(table, "交易对方", 1, "交易对方")
        change_col_place(table, "商品", 2, "商品说明")
        change_col_place(table, "支付方式", 3, "收/付款方式")
        change_col_place(table, "金额(元)", 4, "金额")
        change_col_place(table, "当前状态", 5, "交易状态")
        change_col_place(table, "交易类型", 6, "交易分类")
        change_col_place(table, "交易时间", 7, "交易时间")
        table.drop(columns=["备注", "交易单号", "商户单号"], inplace=True)
        return table

    def write_result_file(self, filename="XXXX年微信收支表.xlsx", output_alipay_format=True):
        result1 = self.read_pay()
        result2 = self.read_income()
        result3 = result1.append(result2, ignore_index=True).reset_index(drop=True)
        if output_alipay_format:
            result3 = self.alipay_format(result3)
        result3["来源"] = "微信"

        writer = pd.ExcelWriter(r"./temp/" + filename)
        result3.to_excel(writer, index=False, sheet_name="收支")
        writer.save()
        writer.close()


def scan_file_wx_csv():
    """
    扫描微信CSV文件
    """
    result = []
    files = FileUtil.scan_file("./source")
    for file in files:
        file_name = file.name
        if file_name.endswith(".csv") and file_name.startswith("微信支付账单"):
            result.append(file)
    return result


def read_wx_record():
    files = scan_file_wx_csv()
    reader = WxExcelReader(files=files)
    reader.write_result_file(filename="微信收支表.xlsx")
