import pandas as pd
from util.file_util import FileUtil
from util.pandas_util import PandasUtil
from handler.alipay_bill_handler import AlipayBillHandler
from handler.wx_bill_handler import WxBillHandler


class Butler:
    """
    管家类
    负责整个项目的调度
    """

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name

    def __get_temp_tables(self, files):
        tables = []
        for file in files:
            if file.name.endswith("xlsx"):
                table = pd.read_excel(file.path)
                tables.append(table)
        return tables

    def start_work(self):
        root_path = FileUtil.get_project_root_path()
        temp_dir_path = root_path + "/temp"
        FileUtil.clean_dir(temp_dir_path)
        FileUtil.clean_dir(root_path + "/target")
        AlipayBillHandler().handle()  # 处理支付宝账单
        WxBillHandler().handle()  # 处理微信账单
        files = FileUtil.scan_file(temp_dir_path)
        tables = self.__get_temp_tables(files)
        result = PandasUtil.merge_tables(tables)
        result.to_excel(
            f"{root_path}/target/{self.output_file_name}", index=False, sheet_name="收支"
        )
        print("\n")
        print("工作完成ヽ(✿ﾟ▽ﾟ)ノヽ(✿ﾟ▽ﾟ)ノ")


output_file_name = "2021年收支表.xlsx"
Butler(output_file_name).start_work()
