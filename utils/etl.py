"""
ETL pipeline for data processing
"""

import pandas as pd


def etl_xlsx(file_xlsx):
    if file_xlsx is not None:
        file_xlsx = pd.read_excel(file_xlsx, engine="openpyxl")
        return file_xlsx
    else:
        return None
