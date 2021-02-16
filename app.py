# Import required libraries

from plots import *
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
                                {'label': 'Combined results', 'value': 'combined'},
                                {'label': 'Barcelogic', 'value': 'barcelogic'},
                                {'label': 'Z3', 'value': 'z3'},
                                {'label': 'OptiMathSAT', 'value': 'oms'}
                            ],
                            value=['combined', 'barcelogic', 'z3', 'oms'],
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='solver'
                        ),
                        html.H5("Choose encoding option:", style={"margin-top" : "15px", "margin-bottom": "10px", "text-align" : "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': 'Initial configuration', 'value': 'initial_configuration'},
                                {'label': 'At most one uninterpreted function', 'value': 'at_most'},
                                {'label': 'Every numerical value must be pushed', 'value': 'pushed_once'},
                                {'label': 'No output before a POP instruction', 'value': 'no_output_before_pop'},
                                {'label': 'Alternative gas model', 'value': 'alternative_gas_model'},
                            ],
                            # value=['initial_configuration', 'at_most', 'pushed_once', 'no_output_before_pop', 'alternative_gas_model'],
                            value=['initial_configuration', 'at_most'],
                            labelStyle={'display': 'inline-block', 'margin-left':'20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='encoding'
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
                            value=[0, 10],
                            id='range',
                            allowCross=False
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


@app.callback([Output('encoding-time', 'figure'), Output('encoding-gas', 'figure'),
               Output('encoding-statistics', 'figure'), Output('encoding-total-times', 'figure')],
              [Input('solver', 'value'), Input('encoding', 'value'), Input('range', 'value')])
def update_stage_one(selected_solvers, selected_encodings, selected_range):
    ctx = dash.callback_context

    change = ctx.triggered[0]['prop_id'].split('.')[0]

    range_figure = plot_total_times(selected_range, selected_solvers, selected_encodings)

    # If we only change the range, then only the last figure must be updated.
    if change == "range":
        return dash.no_update, dash.no_update, dash.no_update, range_figure
    else:
        time_figure = plot_time(selected_solvers, selected_encodings)
        gas_figure = plot_gas(selected_solvers, selected_encodings)
        statistics_figure = plot_statistics(selected_solvers, selected_encodings)
        return time_figure, gas_figure, statistics_figure, range_figure


server = app.server

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
