import itertools

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = (PATH.joinpath("data")).resolve()


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
        fig.add_trace(go.Box(y=times, x=labels, name=encoding))
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
        fig.add_trace(go.Box(y=times, x=labels, name=encoding))
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
                labels_x.append(name)
                labels_y.append(encoding)
                results.append((df[statistic].sum() * 100) / total_sum)
        fig.add_trace(go.Bar(y=results, x=[labels_x, labels_y], name=statistic))
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
    fig.add_trace(go.Box(y=y1, name="Default encoding works better"))
    fig.add_trace(go.Box(y=y2, name="Selected encoding works better"))
    fig.update_layout(yaxis_title="Comparison between encodings")
    return fig
