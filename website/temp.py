import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import random
import datetime
from collections import deque
import os
import csv
import time
from datetime import datetime, timedelta
import threading
from pynput import keyboard, mouse

# CPU Utilization Data
max_length = 50
times_cpu = deque(maxlen=max_length)
cpu_utilizations = deque(maxlen=max_length)

def get_cpu_utilization():
    return random.randint(1, 100)

# Idle Activity Tracking
def str_to_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')

def track_idle_activity(idle_threshold=5, csv_file='idle_times.csv'):
    last_activity_time = time.time()
    idle_start_time = None

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Idle Start Time', 'Idle End Time', 'Idle'])

    def on_activity():
        nonlocal last_activity_time, idle_start_time
        current_time = time.time()
        idle_time = current_time - last_activity_time

        if idle_time > idle_threshold:
            pass
        else:
            if idle_start_time is not None:
                idle_end_time = last_activity_time
                idle_start_str = datetime.fromtimestamp(idle_start_time).strftime('%H:%M:%S')
                idle_end_str = datetime.fromtimestamp(idle_end_time).strftime('%H:%M:%S')
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([idle_start_str, idle_end_str, 1])
                idle_start_time = None

        last_activity_time = current_time

    def check_idle_time():
        nonlocal idle_start_time, last_activity_time
        while True:
            current_time = time.time()
            idle_time = current_time - last_activity_time

            if idle_time > idle_threshold and idle_start_time is None:
                idle_start_time = last_activity_time

            time.sleep(1)

    def on_key_press(key):
        on_activity()

    def on_key_release(key):
        on_activity()

    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

    def on_click(x, y, button, pressed):
        on_activity()

    def on_move(x, y):
        on_activity()

    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

    keyboard_listener.start()
    mouse_listener.start()

    idle_checker_thread = threading.Thread(target=check_idle_time)
    idle_checker_thread.daemon = True
    idle_checker_thread.start()

    keyboard_listener.join()
    mouse_listener.join()

def read_and_process_csv(csv_file='idle_times.csv'):
    if not os.path.exists(csv_file):
        return [], []

    df = pd.read_csv(csv_file)

    times = []
    activity = []

    for i in range(len(df)):
        idle_start = str_to_time(df.loc[i, 'Idle Start Time'])
        idle_end = str_to_time(df.loc[i, 'Idle End Time'])

        if i == 0:
            times.append(idle_start)
            activity.append(1)
        else:
            prev_idle_end = str_to_time(df.loc[i-1, 'Idle End Time'])
            gap_start = prev_idle_end + timedelta(seconds=1)
            while gap_start < idle_start:
                times.append(gap_start)
                activity.append(0)
                gap_start += timedelta(seconds=1)

        current_time = idle_start
        while current_time <= idle_end:
            times.append(current_time)
            activity.append(1)
            current_time += timedelta(seconds=1)

    return times, activity

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Merged Dashboard"),
    html.Div([
        html.Div([
            html.H2("Live CPU Utilization"),
            dcc.Graph(id='live-cpu-graph', animate=True),
            dcc.Interval(
                id='cpu-graph-update',
                interval=1000,
                n_intervals=0
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H2("Idle and Active Periods"),
            dcc.Graph(id='live-idle-graph'),
            dcc.Interval(
                id='idle-interval-component',
                interval=1*1000,
                n_intervals=0
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ])
])

# Define the callback to update the CPU graph
@app.callback(
    Output('live-cpu-graph', 'figure'),
    [Input('cpu-graph-update', 'n_intervals')]
)
def update_cpu_graph(n):
    times_cpu.append(datetime.now())
    cpu_utilizations.append(get_cpu_utilization())

    data = go.Scatter(
        x=list(times_cpu),
        y=list(cpu_utilizations),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data], 'layout': go.Layout(
        xaxis=dict(range=[min(times_cpu), max(times_cpu)]),
        yaxis=dict(range=[0, 100], title='CPU Utilization (%)'),
        title='Time Series'
    )}

# Define the callback to update the idle graph
@app.callback(
    Output('live-idle-graph', 'figure'),
    [Input('idle-interval-component', 'n_intervals')]
)
def update_idle_graph(n):
    times, activity = read_and_process_csv()

    data = [
        go.Scatter(
            x=times,
            y=activity,
            mode='lines+markers',
            line_shape='hv',
            name='Activity'
        )
    ]

    layout = go.Layout(
        xaxis=dict(range=[min(times) if times else datetime.now(), max(times) if times else datetime.now() + timedelta(seconds=1)]),
        yaxis=dict(range=[-0.1, 1.1]),
        title='Idle and Active Periods',
        xaxis_title='Time',
        yaxis_title='Activity',
        showlegend=False
    )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    activity_tracker_thread = threading.Thread(target=track_idle_activity)
    activity_tracker_thread.daemon = True
    activity_tracker_thread.start()

    app.run_server(debug=True)
