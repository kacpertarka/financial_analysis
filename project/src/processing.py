import pandas as pd
from  .reader import DataInfo
import sys
from calendar import monthrange, isleap
from datetime import date





class DataProcessing:

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data


    def get_amount_by_month(self, month: int, category: str = None) -> float:
        """
        Parameters:
          int   - month: the month for wich we are looking for expense
          str   - category: category we are looking for expenses
        Return:
          float:  sum of expenses in the given month
        """
        month_value: pd.DataFrame = self.data[self.data[DataInfo.MONTH] == month]
        if not category:
            return sum(month_value[DataInfo.AMOUNT])
        
        if category not in self.names_of_category():
            raise ValueError("Category does not exists!!!")

        category_mask = self.data[DataInfo.CATEGORY] == category
        category_value = month_value[category_mask]
        return sum(category_value[DataInfo.AMOUNT])


    def get_annual_expenses(self, category: str) -> dict[str: float]:
        """
        Parameters:
          str   - category: category we are looking for expenses
        Return:
          dict[str: float]: dict[month: sum of expenses]
        """
        months_expenses: dict = dict()
        for i in range(1, 13):
            try:
                months_expenses[i] = self.get_amount_by_month(i, category)
            except ValueError as err:
                print(err)
                sys.exit(-1)
        
        return months_expenses

    def names_of_category(self) -> set[str]:
        """
        Return:
          set[str]: set of names category in self.data
        """
        return set(self.data[DataInfo.CATEGORY])
    

    def average(self, month: int = None, category: str = "food") -> float:
        """
        Parameters:
          int   - month: month to find average of expense, if None - return average for whole year
          str   - category: category to find average of expenses
        Return:
          float: average of expenses for month or year
        """
        
        if not month:
            annual_exp: float = sum(self.get_annual_expenses(category).values())
            if isleap(date.today().year):
                return annual_exp / 366
            return annual_exp / 365
        month_exp: float = self.get_amount_by_month(month, category)
        return month_exp / monthrange(date.today().year, month)[1]
        