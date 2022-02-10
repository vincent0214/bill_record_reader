import pandas as pd


class PandasUtil:
    @staticmethod
    def merge_tables(tables):
        """
        合并表格(相同格式,上下合并)
        """
        result = None
        for table in tables:
            if result is None:
                result = table
                continue
            result = result.append(table, ignore_index=True)
        result.reset_index(drop=True)
        return result

    @staticmethod
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
