import sys
import dash.exceptions
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from typing import Any
from src.reader import load_data_from_file, DataInfo
from src.processing import DataProcessing


FILE: str = "data/test.csv"

#
# class App:
#     def run(self) -> None:
#         pass
#
#     def get_month_from_value(self, month: str) -> int:
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
#
#         try:
#             returned_month: int = date_to_date[month]
#         except KeyError as err:
#             print(f"There is not a month named {month}")
#             sys.exit(-1)
#         return returned_month


app = Dash(__name__)


def main() -> None:

    df = load_data_from_file(FILE)
    data = DataProcessing(df)
    x: dict[str: float] = data.get_annual_expenses()
    fig = px.bar(df, x="date", y="amount", color="category")
    chart = px.pie(values=x.values(), names=x.keys())
    print(data.names_of_category())
    category_list = data.names_of_category()
    df2 = pd.DataFrame({
        "Car": ["Mercedes", "Jaguar", "Ford"],
        "Amount": [1, 1, 1],
        "Country": ["Germany", "GB", "USA"]
    })
    fig2 = px.bar(df2, x="Car", y="Amount", color="Country", barmode="group")

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
            html.Div(id="out"),
        ]),

        html.Div(children=[
            dcc.Graph(
                id='example-graph',
                figure=chart,
                style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            ),
            dcc.Graph(
                id='fig',
                figure={},  # fig2
                style={'display': 'inline-block', 'width': '50%', 'height': '60vh'}
            ),
            dcc.Graph(
                id='year-graph',
                figure=fig,
                style={'width': '100%', 'height': '50vh'}
            )
        ]),

    ])

    @app.callback(
        [
            Output(component_id="fig", component_property="figure"),
            Output(component_id="input", component_property="value"),
            Output(component_id="category", component_property="value")
        ],
        Input(component_id="btn", component_property="n_clicks"),
        [
            State(component_id="category", component_property="options"),
            State(component_id="input", component_property="value")
        ]
    )
    def get_value(click: int, category: str, input_value: str):
        if input_value != "":
            # print(input_value)
            print(category)
            dff = df2.copy()
            try:
                dff.loc[0, "Amount"] = float(input_value)
            except ValueError:
                return dash.no_update, "", ""
            fig3 = px.bar(dff, x="Car", y="Amount", color="Country", barmode="group")
            return fig3, "", ""
        else:
            return fig2, "", ""

    app.run_server(debug=True)


if __name__ == '__main__':

    main()
