import pandas as pd
from  .reader import DataInfo
import sys
from calendar import monthrange, isleap
import calendar
from datetime import date


class DataProcessing:

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data


    def get_month_expenses(self, month: int, category: str = None) -> float:
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
        for i in range(0, 12):
            try:
                month: str = int_to_str_month(i)
                months_expenses[month] = self.get_month_expenses(i, category)
            except ValueError as err:
                print(err)
                sys.exit(-1)
        
        return months_expenses

    def names_of_category(self, month: int = None) -> set[str]:
        """
        Return:
          set[str]: set of names category in self.data
        """
        if not month:
          return set(self.data[DataInfo.CATEGORY])
        month_df: pd.DataFrame = self.data[self.data[DataInfo.MONTH] == month]
        return set(month_df[DataInfo.CATEGORY])
    

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
        
    
    def get_month_category_value(self, month: int) -> dict[str, float]:
        """
        Parameter:
          int   - month: month for which we're looking for a expenses by category
        Return:
          list: list of dict with key = category, value = sum of expenses in the given month
        """
        
        month_df: pd.DataFrame = self.data[self.data[DataInfo.MONTH] == month]
        returned_dict: dict = dict()
        category_set: set = self.names_of_category(month=month)

        for category in category_set:
            category_expenses: float = self.get_month_expenses(month, category=category)
            returned_dict[category] = category_expenses
            
        return returned_dict



def int_to_str_month(month: int) -> str:
    months_list: list = list(calendar.month_name[1:])
    try:
        returned_month: str = months_list[month].lower()
    except KeyError as err:
        print(f"There is not a month given by value of {month}")
        sys.exit(-1)
    return returned_month