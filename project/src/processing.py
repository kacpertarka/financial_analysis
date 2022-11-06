import pandas as pd
from  .reader import DataInfo





class DataProcessing:

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_amount_by_month(self, month: int) -> float:

        month_value: pd.DataFrame = self.data[self.data[DataInfo.MONTH] == month]
        return sum(month_value[DataInfo.AMOUNT])
        