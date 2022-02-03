import pandas as pd


class WxExcelReader:
    def __init__(self, file1, file2, file3, file4, output_file=r"./XXXX年微信收支表.xlsx"):
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

    def read(self, file, type):
        """
        file: 收支文件
        type: 收/支类型
        """
        table = pd.read_excel(file, header=16)  # 从17行开始读取, header=0为第1行
        return table.loc[table["收/支"].apply(lambda x: x == type)]

    def read_pay(self):
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
        return result

    def read_income(self):
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
        return result

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


file1 = r"./2021年-01.xlsx"  # 第1季度收支文件
file2 = r"./2021年-04.xlsx"  # 第2季度收支文件
file3 = r"./2021年-07.xlsx"  # 第3季度收支文件
file4 = r"./2021年-10.xlsx"  # 第4季度收支文件
output_file = r"./2021年微信收支表.xlsx"
reader = WxExcelReader(file1, file2, file3, file4, output_file)
reader.write_result_file()
