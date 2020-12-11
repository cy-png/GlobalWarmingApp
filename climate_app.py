import os
import pathlib
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import cufflinks as cf
from temperature_data_analysis import *

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server



YEARS = [1875, 1885, 1895, 1905, 1915, 1925, 1935, 1945, 1955, 1965, 1975, 1985, 1995, 2005, 2013]


# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("global_warming.png")),
                html.H4(children="Does 'global warming' mean it’s warming everywhere?"),
                html.P(
                    id="description",
                    children="No, 'global warming' means Earth's average annual air temperature is rising, but not necessarily in every single location during all seasons across the globe. "
                             "The figure on the left shows the temperature changes in various countries, while the picture on the right shows the change of global average temperature level",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap of global temperature in {}".format(
                                        min(YEARS)
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="country-choropleth",
                                    figure=dict(
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                center=dict(
                                                    lat=38.72490, lon=-95.61446
                                                ),
                                                pitch=0,
                                                zoom=5,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select Month:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Annual",
                                    "value": 0,
                                },
                                {
                                    "label": "Jan",
                                    "value": 1,
                                },
                                {
                                    "label": "Feb",
                                    "value": 2,
                                },
                                {
                                    "label": "Mar",
                                    "value": 3,
                                },
                                {
                                    "label": "Apr",
                                    "value": 4,
                                },
                                {
                                    "label": "May",
                                    "value": 5,
                                },
                                {
                                    "label": "Jun",
                                    "value": 6,
                                },
                                {
                                    "label": "Jul",
                                    "value": 7,
                                },
                                {
                                    "label": "Aug",
                                    "value": 8,
                                },
                                {
                                    "label": "Sep",
                                    "value": 9,
                                },
                                {
                                    "label": "Oct",
                                    "value": 10,
                                },
                                {
                                    "label": "Nov",
                                    "value": 11,
                                },
                                {
                                    "label": "Dec",
                                    "value": 12,
                                },
                            ],
                            value="Choose a month",
                            id="month-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)
@app.callback(
    Output("heatmap-title", "children"),
    [Input("years-slider", "value")]
)
def update_map_title(year):
    return "Heatmap of global temperature in {}".format(year)


@app.callback(
    Output("selected-data", "figure"),
    [Input("month-dropdown", "value")]
)
def update_global_chart(month):
    fig = plot_temperature_monthly(global_temperature,month)
    fig_layout = fig["layout"]
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#f9e7df"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig.update_traces(line_color='#ffbc7d')
    return fig


@app.callback(
    Output("country-choropleth", "figure"),
    [Input("years-slider", "value")]
)
def update_country_chart(year):
    fig = geo_plot(country_temperature,year)
    fig_layout = fig["layout"]
    fig_layout["paper_bgcolor"] = "#212936"
    fig_layout["font"]["color"] = "#ffbc7d"
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    return fig




if __name__ == "__main__":
    app.run_server(debug=True)
