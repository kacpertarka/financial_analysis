import plotly.express as px
from datetime import date
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']


def pie_plot(data: dict[str, float]) -> px.pie:
    """Generate pie plot """
    # TODO try use plotly.graph_objects.Pie instead of px.pie

    pie = px.pie(values=data.values(), names=data.keys())

    return pie


def daily_bar(data: dict[date, float]) -> px.bar:
    """Generate bar plot for daily expenses"""

    plot = px.bar(x=data.keys(), y=data.values(), barmode="group")
    return plot


def monthly_bar(data: dict[str, float]) -> px.bar:
    """Generate bar plot for monthly expenses"""

    plot = px.bar(x=data.keys(), y=data.values(), barmode="group")
    return plot
