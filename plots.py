import itertools

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import pathlib
import plotly.express as px
from plotly.subplots import make_subplots

PATH = pathlib.Path(__file__).parent
DATA_PATH = (PATH.joinpath("data")).resolve()
encoding_names = {'initial_configuration': "Initial configuration",
                  "no_output_before_pop": "Restricted opcodes<br>before POP",
                  'at_most': "Uninterpreted opcodes<br>at most once",
                  'pushed_once': "Numerical values pushed<br>at least once",
                  "alternative_gas_model": "Alternative gas model",
                  "final_encoding": "Final encoding",
                  "60s": "60s", "30s": "30s", "15s": "15s", "10s": "10s", "1s": "1s",
                  "no_output_before_pop_at_most": "Rest. bef. POP +<br> Unint. opcode at most",
                  "no_output_before_pop_pushed_once": "Rest. bef. POP +<br> Num. value once",
                  "no_output_before_pop_at_most_pushed_once": "Rest. bef. POP +<br> Unint. opcode at most"
                                                              "+<br> Num. value once"}

optimality_names = {'already_optimal': "Already optimal", 'discovered_optimal': "Discovered optimal",
                    'non_optimal_with_less_gas': "Non optimal<br> with less gas",
                    'non_optimal_with_same_gas': "Non optimal<br> with same gas",
                    'no_solution_found': "No solution found"}

encoding_names_abbreviated = {'initial_configuration': "initial", "no_output_before_pop": "restrict POP",
                              'at_most': "at most", 'pushed_once': "values pushed",
                              "alternative_gas_model": "alt. gas model", "60s": "60s", "30s": "30s", "15s": "15s",
                              "10s": "10s", "1s": "1s", "final_encoding": "final"}

analyzed_parameters_names = {'saved_gas': "Gas saved", 'time': "Time in min"}

solver_name_abbreviated = {"combined": "port", "z3": "z3", "oms": "oms", "barcelogic": "bclg"}


def plot_time(folder_name, encodings):
    fig = go.Figure()
    for encoding in encodings:
        times = np.empty(0, dtype=float)
        labels = []
        for name in folder_name:
            csv_name = str(DATA_PATH) + "/" + encoding + "_" + name + ".csv"
            df = pd.read_csv(csv_name)
            arr = df['time'].to_numpy() / 60
            times = np.append(times, arr)
            labels.extend([name] * len(arr))
        fig.add_trace(go.Box(y=times, x=labels, name=encoding_names[encoding]))
    fig.update_layout(
        yaxis_title='Times per contract (minutes)',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig


def plot_gas(folder_name, encodings):
    fig = go.Figure()
    for encoding in encodings:
        times = np.empty(0, dtype=float)
        labels = []
        for name in folder_name:
            csv_name = str(DATA_PATH) + "/" + encoding + "_" + name + ".csv"
            df = pd.read_csv(csv_name)
            arr = df['saved_gas'].to_numpy()
            times = np.append(times, arr)
            labels.extend([name] * len(arr))
        fig.add_trace(go.Box(y=times, x=labels, name=encoding_names[encoding]))
    fig.update_layout(
        yaxis_title='Saved gas per contract',
        boxmode='group'  # group together boxes of the different traces for each value of x
    )
    return fig


def plot_statistics(folder_name, encodings):
    fig = go.Figure()
    statistics = ['already_optimal', 'discovered_optimal', 'non_optimal_with_less_gas', 'non_optimal_with_same_gas',
                  'no_solution_found']
    for statistic in statistics:
        labels_x = []
        labels_y = []
        results = []
        for name in folder_name:
            for encoding in encodings:
                csv_name = str(DATA_PATH) + "/" + encoding + "_" + name + ".csv"
                df = pd.read_csv(csv_name)
                total_sum = 0
                for other_statistics in statistics:
                    total_sum += df[other_statistics].sum()
                labels_x.append(solver_name_abbreviated[name])
                labels_y.append(encoding_names_abbreviated[encoding])
                results.append((df[statistic].sum() * 100) / total_sum)
        fig.add_trace(go.Bar(y=results, x=[labels_x, labels_y], name=optimality_names[statistic]))
    fig.update_layout(
        yaxis_title='Comparison in outputs',
        barmode='stack',
    )
    return fig


def select_comparison(df, comparison_category):
    if comparison_category == "init_progr_len":
        return df[comparison_category].to_numpy()
    elif comparison_category == "initial_size_relation":
        return df[comparison_category].to_numpy()
    elif comparison_category == "number_of_necessary_push":
        return df[comparison_category].to_numpy()
    elif comparison_category == "number_of_necessary_uninterpreted_instructions":
        return df[comparison_category].to_numpy()
    elif comparison_category == "push_per_initial":
        return df["number_of_necessary_push"].to_numpy() / df["init_progr_len"].to_numpy()
    elif comparison_category == "uninterpreted_per_initial":
        return df["number_of_necessary_uninterpreted_instructions"].to_numpy() / df["init_progr_len"].to_numpy()
    elif comparison_category == "push_per_expected":
        expected_size = np.array(list(map(lambda x: 1 if x == 0 else x, df['inferred_size'])))
        return df["number_of_necessary_push"].to_numpy() / expected_size
    elif comparison_category == "uninterpreted_per_expected":
        expected_size = np.array(list(map(lambda x: 1 if x == 0 else x, df['inferred_size'])))
        return df["number_of_necessary_uninterpreted_instructions"].to_numpy() / expected_size


def plot_comparison(cat1, cat2, relation):
    csv_name1 = str(DATA_PATH) + "/" + "comparison_" + cat1 + "_" + cat2 + ".csv"
    csv_name2 = str(DATA_PATH) + "/" + "comparison_" + cat2 + "_" + cat1 + ".csv"
    y1 = select_comparison(pd.read_csv(csv_name1), relation)
    y2 = select_comparison(pd.read_csv(csv_name2), relation)
    fig = go.Figure()
    fig.add_trace(go.Box(y=y1, name="Default encoding works better", boxpoints='all', marker_size=3))
    fig.add_trace(go.Box(y=y2, name="Selected encoding works better", boxpoints='all', marker_size=3))
    fig.update_layout(yaxis_title="Comparison between encodings")
    return fig


def plot_configuration_comparison(category_comparison, axis_label):
    csv_name = str(DATA_PATH) + "/" + category_comparison + "_parameter_comparison.csv"
    df = pd.read_csv(csv_name)
    x = [encoding_names[encoding] for encoding in df['name'].to_list()]
    y = df['time'].to_list()
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(yaxis_title=axis_label)
    return fig


def plot_statistics_pie_chart(solver):
    syrup_csv_name = str(DATA_PATH) + "/final_encoding_" + solver + ".csv"
    cav_csv_name = str(DATA_PATH) + "/CAV_" + solver + ".csv"
    labels = ['already_optimal', 'discovered_optimal', 'non_optimal_with_less_gas',
              'non_optimal_with_same_gas', 'no_solution_found']
    labels_to_desplay = [optimality_names[name] for name in labels]
    cav_df = pd.read_csv(cav_csv_name).sum()
    syrup_df = pd.read_csv(syrup_csv_name).sum()

    cav_values = [cav_df[label] for label in labels]
    syrup_values = [syrup_df[label] for label in labels]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels_to_desplay, values=cav_values, name="CAV'20 Setup"),
                  1, 1)
    fig.add_trace(go.Pie(labels=labels_to_desplay, values=syrup_values, name="New setup"),
                  1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Comparison between CAV'20 Setup (15 min) vs New setup (10 s)",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='15m', x=0.18, y=0.5, font_size=20, showarrow=False),
                     dict(text='10s', x=0.82, y=0.5, font_size=20, showarrow=False)])
    return fig


def plot_bar_comparison(solver, category_name):
    syrup_csv_name = str(DATA_PATH) + "/final_encoding_" + solver + ".csv"
    cav_csv_name = str(DATA_PATH) + "/CAV_" + solver + ".csv"
    cav_rows = pd.read_csv(cav_csv_name).to_dict('records')
    syrup_rows = pd.read_csv(syrup_csv_name).to_dict('records')
    labels = list(range(len(syrup_rows)))
    cav_values = []
    syrup_values = []
    for i, cav_row in enumerate(cav_rows):
        block_name = cav_row['name']
        syrup_row = list(filter(lambda row: row['name'] == block_name, syrup_rows))[0]
        if category_name == "time":
            cav_values.append(cav_row[category_name] / 60)
            syrup_values.append(syrup_row[category_name] / 60)
        else:
            cav_values.append(cav_row[category_name])
            syrup_values.append(syrup_row[category_name])
    fig = go.Figure(data=[go.Bar(name="CAV'20 Setup", x=labels, y=cav_values),
                          go.Bar(name='New Setup', x=labels, y=syrup_values)])
    fig.update_layout(barmode='group', yaxis_title=analyzed_parameters_names[category_name] + ' per contract',)
    return fig
