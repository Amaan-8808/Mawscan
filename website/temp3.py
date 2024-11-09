import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import random
from collections import deque
import threading
from pynput import keyboard, mouse
import time  # Import the time module

# CPU Utilization Data
max_length = 50
times_cpu = deque(maxlen=max_length)
cpu_utilizations = deque(maxlen=max_length)

# Global DataFrame to store idle times
idle_df = pd.DataFrame(columns=['Timestamp', 'Activity'])

def get_cpu_utilization():
    return random.randint(1, 100)

# Idle Activity Tracking
def track_idle_activity():
    global idle_df  # Declare idle_df as a global variable

    def log_activity(activity):
        global idle_df  # Declare idle_df as a global variable within the function
        current_time = pd.Timestamp.now()
        new_data = pd.DataFrame({'Timestamp': [current_time], 'Activity': [activity]})
        idle_df = pd.concat([idle_df, new_data], ignore_index=True)

    def on_activity():
        log_activity(1)

    def check_idle_time():
        while True:
            current_time = pd.Timestamp.now()
            if len(idle_df) > 0:
                idle_time = current_time - idle_df['Timestamp'].iloc[-1]
                if idle_time.total_seconds() > 5:
                    log_activity(0)
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

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
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
    times_cpu.append(pd.Timestamp.now())
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
    global idle_df

    times = idle_df['Timestamp']
    activity = idle_df['Activity']

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
        xaxis=dict(range=[min(times) if len(times) > 0 else pd.Timestamp.now(), max(times) if len(times) > 0 else pd.Timestamp.now() + pd.Timedelta(seconds=1)]),
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
