import sys
import dash.exceptions
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from src.reader import load_data_from_file, DataInfo, add_data_to_file
from src.processing import DataProcessing, CATEGORY_LIST

FILE: str = "data/test.csv"


#     def get_month_from_value(month: str) -> int:
#         date_to_date: dict[str: int] = {
#             "january": 1,
#             "february": 2,
#             "march": 3,
#             "april": 4,
#             "may": 5,
#             "june": 6,
#             "july": 7,
#             "august": 8,
#             "september": 9,
#             "october": 10,
#             "november": 11,
#             "december": 12
#         }


app = Dash(__name__)


def main() -> None:

    df: pd.DataFrame = load_data_from_file(FILE)
    data = DataProcessing(df)
    category_list = CATEGORY_LIST
    # current_month_expenses = data.get_month_category_value(current_month)
    # fig = px.bar(df, x="date", y="amount", color="category")
    # chart = px.pie(values=annual_expenses.values(), names=annual_expenses.keys())

    # curren_month =

    # monthly_expenses_fig = px.bar(x=current_month_expenses.keys(), y=current_month_expenses.values(), barmode="group")
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children=[
            dcc.Input(
                id="input",
                value="",
                type="text",
                placeholder="Amount",
                style={'display': 'inline-block', 'width': '300px', 'height': '15px'}
            ),
            dcc.Dropdown(
                id="category",
                options=category_list,
                value="",
                placeholder="Select category",
                style={'display': 'inline-block', 'width': '300px', 'height': '30px'}
            ),
            html.Button(
                id="btn", n_clicks=0, type="submit", children="Submit"
            ),
            html.Div(id="out")
        ]
        ),

        html.Div(children=[
            # dcc.Graph(
            #     id='annual-expenses-chart',
            #     figure=chart,
            #     style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            # ),
            dcc.Graph(
                id='monthly-expenses-bar',
                figure={},  # fig2
                style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            ),
            # dcc.Graph(
            #     id='daily-expenses-graph',
            #     figure={},
            #     style={'width': '100%', 'height': '50vh'}
            # )
        ]),

    ])

    @app.callback(
        [
            Output(component_id="monthly-expenses-bar", component_property="figure"),
            Output(component_id="input", component_property="value"),
            Output(component_id="category", component_property="value")
        ],
        Input(component_id="btn", component_property="n_clicks"),
        [
            State(component_id="category", component_property="value"),
            State(component_id="input", component_property="value")
        ]
    )
    def get_value(_: int, category: str, input_value: str) -> tuple:
        current_month = datetime.today().month
        filtered_data: dict[str, float] = data.get_month_category_value(current_month)
        monthly_expenses_fig = px.bar(x=filtered_data.keys(), y=filtered_data.values(), barmode="group")
        if input_value != "":
            try:
                amount = int(input_value)
            except ValueError:
                return monthly_expenses_fig, "", ""
            current_date = datetime.today().strftime("%Y-%m-%d")
            adding_value = {
                DataInfo.DATE: [current_date],
                DataInfo.AMOUNT: [amount],
                DataInfo.CATEGORY: [category],
                DataInfo.YEAR: [datetime.today().year],
                DataInfo.MONTH: [current_month],
                DataInfo.DAY: [datetime.today().day]
            }
            add_data_to_file(FILE, adding_value, df)
            new_df = concat(adding_value, df)
            print(df)
            print(new_df)
            new_data = DataProcessing(new_df)
            filtered_data: dict[str, float] = new_data.get_month_category_value(current_month)
            monthly_expenses_fig = px.bar(x=filtered_data.keys(), y=filtered_data.values(), barmode="group")
            return monthly_expenses_fig, "", ""
        return monthly_expenses_fig, "", ""

    app.run_server(debug=True)


def concat(new_val: dict, old_val: pd.DataFrame) -> pd.DataFrame:
    """Concat dictionary to DataFrame & cut"""
    new_df = pd.DataFrame.from_dict(data=new_val)
    new_df = pd.concat([new_df, old_val], axis=0, ignore_index=True)
    new_df.astype({DataInfo.YEAR: 'int', DataInfo.MONTH: 'int', DataInfo.DAY: 'int'})
    return new_df


if __name__ == '__main__':

    main()
