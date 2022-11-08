import sys
from src.reader import load_data_from_file, DataInfo
from src.processing import DataProcessing


FILE: str = "data/test.csv"


class App:

    def run(self) -> None:

        data: pd.DataFrame = load_data_from_file(FILE)
        # print(data)

        process: object = DataProcessing(data)

        

        integer_month: int = self.get_month_from_value("november")
        # process.names_of_category()
        # print(process.get_amount_by_month(integer_month, "food"))
        # d = process.get_annual_expenses("food")
        # print(d)
        print(process.average(11))

    def get_month_from_value(self, month: str) -> str:
        date_to_date: dict[str: int] = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12
        }
        
        try:
            returned_month: int = date_to_date[month]
        except KeyError as err:
            print(f"There is not a month named {month}")
            sys.exit(-1)
        return returned_month




def main() -> None:

    app: object = App()

    app.run()

   


if __name__ == '__main__':

    main()

