import pandas as pd
import copy


class WxExcelReader:
    def __init__(
        self,
        file1,
        file2,
        file3,
        file4,
        output_file=r"./XXXX年微信收支表.xlsx",
        output_alipay_excel_format=True,
    ):
        """
        file1: 第1季度收支文件
        file2: 第2季度收支文件
        file3: 第3季度收支文件
        file4: 第4季度收支文件
        """
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3
        self.file4 = file4
        self.output_file = output_file
        self.output_alipay_excel_format = output_alipay_excel_format

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

    def read(self, file, type):
        """
        file: 收支文件
        type: 收/支类型
        """
        table = self.get_table(file)
        return table.loc[table["收/支"].apply(lambda x: x == type)]

    def read_pay(self):
        """
        读取支出
        """
        r1_1 = self.read(self.file1, "支出")
        r1_2 = self.read(self.file2, "支出")
        r1_3 = self.read(self.file3, "支出")
        r1_4 = self.read(self.file4, "支出")
        result = (
            r1_1.append(r1_2, ignore_index=True)
            .append(r1_3, ignore_index=True)
            .append(r1_4, ignore_index=True)
            .reset_index(drop=True)
        )
        result.sort_values("交易时间", inplace=True)
        if self.output_alipay_excel_format:
            result = self.change_wx_excel_to_alipay_excel(result)
        return result

    def read_income(self):
        """
        读取收入
        """
        r2_1 = self.read(self.file1, "收入")
        r2_2 = self.read(self.file2, "收入")
        r2_3 = self.read(self.file3, "收入")
        r2_4 = self.read(self.file4, "收入")
        result = (
            r2_1.append(r2_2, ignore_index=True)
            .append(r2_3, ignore_index=True)
            .append(r2_4, ignore_index=True)
            .reset_index(drop=True)
        )
        result.sort_values("交易时间", inplace=True)
        if self.output_alipay_excel_format:
            result = self.change_wx_excel_to_alipay_excel(result)
        return result

    def change_wx_excel_to_alipay_excel(self, table):
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
        change_col_place(table, "支付方式", 3, "收付方式")
        change_col_place(table, "金额(元)", 4, "金额")
        change_col_place(table, "当前状态", 5, "交易状态")
        change_col_place(table, "交易类型", 6, "交易分类")
        change_col_place(table, "交易时间", 7, "交易时间")
        table.drop(labels=["交易单号"], axis=1, inplace=True)
        table.drop(labels=["商户单号"], axis=1, inplace=True)
        table.drop(labels=["备注"], axis=1, inplace=True)
        return table

    def write_result_file(self):
        result1 = self.read_pay()
        result2 = self.read_income()
        result3 = result1.append(result2, ignore_index=True).reset_index(drop=True)

        writer = pd.ExcelWriter(self.output_file)
        result3.to_excel(writer, index=False, sheet_name="收支")
        result1.to_excel(writer, index=False, sheet_name="支出")
        result2.to_excel(writer, index=False, sheet_name="收入")

        writer.save()
        writer.close()


# 支持读取excel文件和csv文件
file1 = r"./2021年-01.xlsx"  # 第1季度收支文件
file2 = r"./2021年-04.xlsx"  # 第2季度收支文件
file3 = r"./2021年-07.xlsx"  # 第3季度收支文件
file4 = r"./2021年-10.xlsx"  # 第4季度收支文件
output_file = r"./2021年微信收支表.xlsx"
output_alipay_excel_format = True  # 是否输出支付宝excel格式, 如果为False输出微信格式
reader = WxExcelReader(
    file1, file2, file3, file4, output_file, output_alipay_excel_format
)
reader.write_result_file()
