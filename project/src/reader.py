import pandas as pd
# from datetime import datetime


class DataInfo:
    CATEGORY = "category"
    AMOUNT: str = "amount"
    DATE: str = "date"
    YEAR: str = "year"
    MONTH: str = "month"
    DAY: str = "day"


def load_data_from_file(file_path: str) -> pd.DataFrame:
    """Read from csv file"""
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


def add_data_to_file(file_path: str, data: dict, old_data: pd.DataFrame) -> None:
    """Save value to csv file"""
    df = pd.DataFrame.from_dict(data=data)
    new_value = pd.concat([df, old_data], axis=0, ignore_index=True)
    new_value = new_value.loc[:, [DataInfo.DATE, DataInfo.AMOUNT, DataInfo.CATEGORY]]
    # print(new_value.loc[:, [DataInfo.DATE, DataInfo.AMOUNT, DataInfo.CATEGORY]])
    new_value.to_csv(file_path, index=False, header=True, sep=";")
