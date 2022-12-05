import pandas as pd
from datetime import datetime

class DataInfo:

    CATEGORY: str = "category"
    AMOUNT: str = "amount"
    DATE: str = "date"
    YEAR: str = "year"
    MONTH: str = "month"
    DAY: str = "day"



def load_data_from_file(file_path: str) -> pd.DataFrame:

    data = pd.read_csv(file_path, 
                        sep=";", 
                        dtype={
                            DataInfo.AMOUNT: float,
                            DataInfo.CATEGORY: str,
                        },
                        parse_dates=[DataInfo.DATE])
    data[DataInfo.DATE] = pd.to_datetime(data[DataInfo.DATE]).dt.date
    data[DataInfo.YEAR] = pd.DatetimeIndex(data[DataInfo.DATE]).year.astype(int)
    data[DataInfo.MONTH] = pd.DatetimeIndex(data[DataInfo.DATE]).month.astype(int)
    data[DataInfo.DAY] = pd.DatetimeIndex(data[DataInfo.DATE]).day.astype(int)
   
    return data
