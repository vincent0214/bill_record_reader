import imp


import pandas as pd


class PandasUtil:
    @staticmethod
    def merge_tables(tables):
        result = None
        for table in tables:
            if result is None:
                result = table
            result = result.append(table, ignore_index=True)
        result.reset_index(drop=True)
        return result
