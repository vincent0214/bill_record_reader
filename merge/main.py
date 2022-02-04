import pandas as pd


table_1 = pd.read_excel("./2021年支付宝收支表.xlsx")
table_2 = pd.read_excel("./2021年微信收支表.xlsx")
table_1["来源"] = "支付宝"
table_2["来源"] = "微信"
table = table_1.append(table_2, ignore_index=True).reset_index(drop=True)
# table.sort_values("交易时间", inplace=True)
table.to_excel("./2021-收支表.xlsx", index=False, sheet_name="收支")
