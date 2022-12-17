import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from src.reader import load_data_from_file, DataInfo, add_data_to_file
from src.processing import DataProcessing, CATEGORY_LIST
from src.plots import pie_plot, monthly_bar, daily_bar
from datetime import date


FILE: str = "data/test.csv"

#
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
    current_month = datetime.today().month

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
            html.H4("Annual expenses by category"),
            dcc.Graph(
                id='annual-expenses-chart',
                figure={},
                style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            ),
            dcc.Graph(
                id='monthly-expenses-bar',
                figure={},  # fig2
                style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            ),
            dcc.Graph(
                id='daily-expenses-graph',
                figure={},
                style={'width': '100%', 'height': '50vh'}
            )
        ]),
    ])

    @app.callback(
        [
            Output(component_id="monthly-expenses-bar", component_property="figure"),
            Output(component_id="daily-expenses-graph", component_property="figure"),
            Output(component_id="annual-expenses-chart", component_property="figure"),
            Output(component_id="input", component_property="value"),
            Output(component_id="category", component_property="value"),
        ],
        Input(component_id="btn", component_property="n_clicks"),
        [
            State(component_id="category", component_property="value"),
            State(component_id="input", component_property="value")
        ]
    )
    def get_value(_: int, category: str, input_value: str) -> tuple:
        """Get value from input and return plots"""
        # get data for plots
        monthly_expenses: dict[str, float] = data.get_month_category_value(current_month)
        daily_expenses: dict[date, float] = data.daily_expenses()
        annual_expenses: dict[str, float] = data.annual_expenses()
        # generate plots
        monthly_expenses_fig = monthly_bar(monthly_expenses)
        daily_expenses_fig = daily_bar(daily_expenses)
        chart_pic = pie_plot(annual_expenses)
        if input_value != "" and input_value is not None:
            try:
                amount = round(float(input_value.replace(",", ".")), 2)
            except ValueError:
                return monthly_expenses_fig, daily_expenses_fig, "", ""
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
            new_df = load_data_from_file(FILE)
            new_data = DataProcessing(new_df)
            # get data for plots
            monthly_expenses: dict[str, float] = new_data.get_month_category_value(current_month)
            daily_expenses: dict[date, float] = new_data.daily_expenses()
            annual_expenses: dict[str, float] = new_data.annual_expenses()
            # generate plots
            monthly_expenses_fig = monthly_bar(monthly_expenses)
            daily_expenses_fig = daily_bar(daily_expenses)
            chart_pic = pie_plot(annual_expenses)
            return monthly_expenses_fig, daily_expenses_fig, chart_pic, "", ""
        else:
            return monthly_expenses_fig, daily_expenses_fig, chart_pic, "", ""

    app.run_server(debug=True)


if __name__ == '__main__':

    main()
