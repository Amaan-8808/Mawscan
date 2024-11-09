import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import threading
import csv
import time
from pynput import keyboard, mouse

# Function to convert time string to datetime object
def str_to_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')

# Function to track idle activity
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
                print(f"Idle from {idle_start_str} to {idle_end_str}")

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
                print("REACHED THRESHOLD")

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
    html.H1("Idle and Active Periods"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    )
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):
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
