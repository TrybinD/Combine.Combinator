import pandas as pd

class ExcelParseService:

    @staticmethod
    def parse_excel(excel_file: bytes):
        df = pd.read_excel(excel_file, header=0)

        print(df)

        return df.to_dict('index')
