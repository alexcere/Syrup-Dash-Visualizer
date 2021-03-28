#!/usr/bin/python3
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

labels_configuration = {'init': 'Initial program length <= 15', 'size_relation':
    'Relation between program length lower bound and initial program length >= 0.7',
                        'number_push': 'Number of necessary PUSHx instructions <= 3',
                        'uninterpreted_per_initial': 'Relation between number of necessary uninterpreted instructions '
                                                     'and initial program length >= 0.25'}

app.title = "Syrup Data Visualizer"
# Create app layout
app.layout = html.Div(
    [
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
            style={"margin-bottom": "25px", "text-align": "center"}, ),
        html.Div(
            [
                html.H3("Stage one: Determining the best encoding"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.H4("1.1 Initial study on different encodings"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose solver option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
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
                        html.H5("Choose encoding option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': 'Initial configuration', 'value': 'initial_configuration'},
                                {'label': 'At most one uninterpreted function', 'value': 'at_most'},
                                {'label': 'Every numerical value must be pushed', 'value': 'pushed_once'},
                                {'label': 'No output before a POP instruction', 'value': 'no_output_before_pop'},
                                {'label': 'Alternative gas model', 'value': 'alternative_gas_model'},
                            ],
                            value=['initial_configuration', 'at_most'],
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
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
                html.H4("1.2 Determine possible parameters that affect the encoding"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div([
                    html.H5("Choose category to compare against no output before pop:",
                            style={"margin-top": "15px", "margin-bottom": "10px",
                                   "text-align": "center"}),
                    dcc.RadioItems(
                        options=[
                            {'label': 'No output before pop + at most',
                             'value': 'no_output_before_pop_at_most'},
                            {'label': 'No output before pop + pushed once',
                             'value': 'no_output_before_pop_pushed_once'},
                            {'label': 'No output before pop + at most + pushed once',
                             'value': 'no_output_before_pop_at_most_pushed_once'},
                        ],
                        value='no_output_before_pop_at_most_pushed_once',
                        labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                        style={'text-align': "center"},
                        inputStyle={"margin-right": "5px"},
                        id='category_1'
                    ),
                    html.H5("Choose comparison filter:",
                            style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Initial program length', 'value': 'init_progr_len'},
                            {'label': 'Relation between program length lower bound and initial '
                                      'program length', 'value': 'initial_size_relation'},
                            {'label': 'Number of necessary PUSHx instructions',
                             'value': 'number_of_necessary_push'},
                            {'label': 'Number of necessary uninterpreted instructions',
                             'value': 'number_of_necessary_uninterpreted_instructions'},
                            {'label': 'Relation between number of necessary PUSHx instructions and '
                                      'initial program length', 'value': 'push_per_initial'},
                            {'label': 'Relation between number of necessary uninterpreted instructions and '
                                      'initial program length', 'value': 'uninterpreted_per_initial'},
                            {'label': 'Relation between number of necessary PUSHx instructions and '
                                      'program length lower bound', 'value': 'push_per_expected'},
                            {'label': 'Relation between number of necessary uninterpreted instructions and '
                                      'program length lower bound', 'value': 'uninterpreted_per_expected'},
                        ],
                        value='init_progr_len',
                        labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                        style={'text-align': "center"},
                        inputStyle={"margin-right": "5px"},
                        id='comparison'
                    ),
                ],
                    className=" pretty_container five columns"),
                html.Div(
                    [
                        html.H4("Comparison between two encodings according to static parameters",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.Loading(dcc.Graph(id='comparison-times'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H4("1.3 Study configurations in which selected encoding seems to work better"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose configuration option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.RadioItems(
                            options=[
                                {'label': labels_configuration['init'], 'value': 'init'},
                                {'label': labels_configuration['size_relation'], 'value': 'size_relation'},
                                {'label': labels_configuration['number_push'], 'value': 'number_push'},
                                {'label': labels_configuration['uninterpreted_per_initial'],
                                 'value': 'uninterpreted_per_initial'}
                            ],
                            value='init',
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='configuration-selection'
                        ),
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='comparison-total-time'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H3("1.4 Final comparison between different steps"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose solver option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
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
                            id='solver-final-stage-one'
                        ),
                        html.H5("Choose encoding option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': 'Initial configuration', 'value': 'initial_configuration'},
                                {'label': 'No output before a POP instruction', 'value': 'no_output_before_pop'},
                                {'label': 'Final selected encoding (no output before pop + '
                                          'pushed once in certain situations)', 'value': '60s'}
                            ],
                            value=['initial_configuration', 'no_output_before_pop', '60s'],
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='encoding-final-stage-one'
                        ),
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='time-final-stage-one'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='statistics-final-stage-one'))
                    ],
                    className="pretty_container five columns"
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='gas-final-stage-one'))
                    ],
                    className="pretty_container seven columns"
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H3("Stage two: Determining the most suitable timeout"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose solver option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
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
                            id='solver-stage-two'
                        ),
                        html.H5("Choose timeout option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.Checklist(
                            options=[
                                {'label': '1 s', 'value': '1s'},
                                {'label': '10 s', 'value': '10s'},
                                {'label': '15 s', 'value': '15s'},
                                {'label': '30 s', 'value': '30s'},
                                {'label': '60 s', 'value': '60s'},
                            ],
                            value=['1s', '30s', '60s'],
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='timeout-stage-two'
                        ),
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-time-stage-two'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-statistics-stage-two'))
                    ],
                    className="pretty_container five columns"
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='encoding-gas-stage-two'))
                    ],
                    className="pretty_container seven columns"
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H3("Stage three: Comparison with CAV benchmark"),
            ],
            style={"margin-top": "25px", "margin-bottom": "25px", "text-align": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5("Choose solver option:",
                                style={"margin-top": "15px", "margin-bottom": "10px", "text-align": "center"}),
                        dcc.RadioItems(
                            options=[
                                {'label': 'Combined results', 'value': 'combined'},
                                {'label': 'Barcelogic', 'value': 'barcelogic'},
                                {'label': 'Z3', 'value': 'z3'},
                                {'label': 'OptiMathSAT', 'value': 'oms'}
                            ],
                            value='combined',
                            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                            style={'text-align': "center"},
                            inputStyle={"margin-right": "5px"},
                            id='solver-stage-three'
                        ),
                    ],
                    className="pretty_container five columns"),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='statistics-stage-three'))
                    ],
                    className="pretty_container seven columns"),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='gas-comparison-stage-three'))
                    ],
                    className="pretty_container twelve columns"
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='time-comparison-stage-three'))
                    ],
                    className="pretty_container twelve columns"
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback([Output('encoding-time', 'figure'), Output('encoding-gas', 'figure'),
               Output('encoding-statistics', 'figure')],
              [Input('solver', 'value'), Input('encoding', 'value')])
def update_stage_one(selected_solvers, selected_encodings):
    time_figure = plot_time(selected_solvers, selected_encodings)
    gas_figure = plot_gas(selected_solvers, selected_encodings)
    statistics_figure = plot_statistics(selected_solvers, selected_encodings)
    return time_figure, gas_figure, statistics_figure


@app.callback(Output('comparison-times', 'figure'),
              [Input('category_1', 'value'), Input('comparison', 'value')])
def update_comparison(category, comparison):
    return plot_comparison("no_output_before_pop", category, comparison)


@app.callback(Output('comparison-total-time', 'figure'), Input('configuration-selection', 'value'))
def update_configuration_study(selected_parameter):
    return plot_configuration_comparison(selected_parameter, labels_configuration[selected_parameter])


@app.callback([Output('time-final-stage-one', 'figure'), Output('gas-final-stage-one', 'figure'),
               Output('statistics-final-stage-one', 'figure')],
              [Input('solver-final-stage-one', 'value'), Input('encoding-final-stage-one', 'value')])
def update_stage_one_final_comparison(selected_solvers, selected_encodings):
    time_figure = plot_time(selected_solvers, selected_encodings)
    gas_figure = plot_gas(selected_solvers, selected_encodings)
    statistics_figure = plot_statistics(selected_solvers, selected_encodings)
    return time_figure, gas_figure, statistics_figure


@app.callback([Output('encoding-time-stage-two', 'figure'), Output('encoding-gas-stage-two', 'figure'),
               Output('encoding-statistics-stage-two', 'figure')],
              [Input('solver-stage-two', 'value'), Input('timeout-stage-two', 'value')])
def update_stage_two(selected_solvers, selected_timeout):
    selected_timeout = sorted(selected_timeout, key=lambda t: t[:-1])
    time_figure = plot_time(selected_solvers, selected_timeout)
    gas_figure = plot_gas(selected_solvers, selected_timeout)
    statistics_figure = plot_statistics(selected_solvers, selected_timeout)
    return time_figure, gas_figure, statistics_figure


@app.callback([Output('statistics-stage-three', 'figure'), Output('gas-comparison-stage-three', 'figure'),
               Output('time-comparison-stage-three', 'figure')],
              Input('solver-stage-three', 'value'))
def update_stage_three(solver):
    statistics_figure = plot_statistics_pie_chart(solver)
    return statistics_figure, go.Figure(), go.Figure()


server = app.server

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
