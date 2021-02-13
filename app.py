# Import required libraries
import base64
import io
import os
import pathlib
from os import listdir
from os.path import join, isfile
from PIL import Image
import matplotlib.image as mpimg
from dash.exceptions import PreventUpdate
from plots import *
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = (PATH.joinpath("data")).resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.title="Syrup Data Visualizer"
# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="current-gray"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Syrup Data Visualizer",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H4(
                            "A detailed analysis on determining the best options for including Syrup in a compiler",
                            style={"margin-top": "0px"}
                        ),
                    ]
                )
            ],
            id="header",
            style={"margin-bottom": "25px", "text-align" : "center"},),
        html.Div(
            [
                html.H3("Stage one: Determining the best encoding"),
            ],
            style={"margin-top" : "25px", "margin-bottom": "25px", "text-align" : "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose solver option:", style={"margin-top" : "15px", "margin-bottom": "10px", "text-align" : "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': 'Combined results', 'value': 'cr'},
                                {'label': 'Barcelogic', 'value': 'barcelogic'},
                                {'label': 'Z3', 'value': 'z3'},
                                {'label': 'OptiMathSAT', 'value': 'oms'}
                            ],
                            value=['cr', 'barcelogic', 'z3', 'oms'],
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"}
                        ),
                        html.H5("Choose encoding option:", style={"margin-top" : "15px", "margin-bottom": "10px", "text-align" : "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': 'Initial configuration', 'value': 'initial'},
                                {'label': 'At most one uninterpreted function', 'value': 'at_most'},
                                {'label': 'Every numerical value must be pushed', 'value': 'pushed'},
                                {'label': 'No output before a POP instruction', 'value': 'no_output'},
                                {'label': 'Alternative gas model', 'value': 'gas'},
                            ],
                            value=['initial', 'at_most', 'pushed', 'no_output', 'gas'],
                            labelStyle={'display': 'inline-block', 'margin-left':'20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"}
                        ),
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-time'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-statistics'))
                    ],
                    className="pretty_container five columns"
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-gas'))
                    ],
                    className="pretty_container seven columns"
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Filter by relation between number of necessary instructions divided by initial number of instructions:",
                                style={"margin-top" : "15px", "margin-bottom": "30px", "text-align" : "center"}),
                        dcc.RangeSlider(
                            marks={i: '{}%'.format(i*10) for i in range(0, 11)},
                            min=0,
                            max=10,
                            value=[0, 10]
                        )
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-total-times'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

server = app.server

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
