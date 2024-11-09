import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import random
from collections import deque
import threading
from pynput import keyboard, mouse
import time
import psutil
from datetime import datetime
from collections import deque
from threading import Thread, Lock
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# CPU Utilization Data
max_length = 50
times_cpu = deque(maxlen=max_length)
cpu_utilizations = deque(maxlen=max_length)

# Global DataFrame to store idle times
idle_df = pd.DataFrame(columns=['Timestamp', 'Activity'])

# In-memory data structure to store network connection data
network_data = deque(maxlen=20)
network_data_lock = Lock()

def get_cpu_utilization():
    return random.randint(1, 100)

# Idle Activity Tracking
def track_idle_activity():
    global idle_df

    def log_activity(activity):
        global idle_df
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

# Function to collect network data
def collect_network_data():
    while True:
        connections = psutil.net_connections(kind='inet')
        connection_count = len(connections)
        timestamp = datetime.now().isoformat()
        with network_data_lock:
            network_data.append({'timestamp': timestamp, 'connection_count': connection_count})
        time.sleep(2)

# Start the network data collection in a background thread
network_data_thread = Thread(target=collect_network_data)
network_data_thread.daemon = True
network_data_thread.start()

# Function to get process information
def get_process_info():
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = proc.info
            processes.append({
                'name': process_info['name'],
                'cpu_percent': process_info['cpu_percent'],
                'memory_percent': process_info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Define the app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("System Monitoring Dashboard"), width=12, className="text-center my-4"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Live CPU Utilization"),
                                dbc.CardBody(
                                    dcc.Graph(id='live-cpu-graph', animate=True)
                                ),
                                dcc.Interval(
                                    id='cpu-graph-update',
                                    interval=1000,
                                    n_intervals=0
                                ),
                            ],
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Idle and Active Periods"),
                                dbc.CardBody(
                                    dcc.Graph(id='live-idle-graph')
                                ),
                                dcc.Interval(
                                    id='idle-interval-component',
                                    interval=1000,
                                    n_intervals=0
                                ),
                            ],
                        ),
                    ],
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Network Connections Over Time"),
                                dbc.CardBody(
                                    dcc.Graph(id='connections-graph')
                                ),
                                dcc.Interval(
                                    id='network-interval-component',
                                    interval=2000,
                                    n_intervals=0
                                ),
                            ],
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Process Information"),
                                dbc.CardBody(
                                    dash_table.DataTable(
                                        id='process-table',
                                        columns=[
                                            {'name': 'Process Name', 'id': 'name'},
                                            {'name': 'CPU Usage (%)', 'id': 'cpu_percent'},
                                            {'name': 'Memory Usage (%)', 'id': 'memory_percent'}
                                        ],
                                        style_cell={'textAlign': 'left'},
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        },
                                        style_table={
                                            'maxHeight': '300px',
                                            'overflowY': 'scroll'
                                        }
                                    ),
                                    style={'margin-top': '50px'}  # Add margin-top to create space between header and table
                                ),
                                dcc.Interval(
                                    id='process-interval-component',
                                    interval=5000,
                                    n_intervals=0
                                ),
                            ],
                        ),
                    ],
                    width=6,
                ),
            ],
        ),
    ],
    fluid=True,
)

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
        # title='Time Series'
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
        # title='Idle and Active Periods',
        xaxis_title='Time',
        yaxis_title='Activity',
        showlegend=False
    )

    return {'data': data, 'layout': layout}

# Callback to update the network connections graph
@app.callback(
    Output('connections-graph', 'figure'),
    [Input('network-interval-component', 'n_intervals')]
)
def update_network_graph(n):
    with network_data_lock:
        timestamps = [item['timestamp'] for item in network_data]
        connection_counts = [item['connection_count'] for item in network_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=connection_counts,
        mode='lines+markers'
    ))
    fig.update_layout(
        # title='Network Connections Over Time',
        xaxis_title='Time',
        yaxis_title='Number of Connections'
    )
    return fig

# Callback to update the process table
@app.callback(
    Output('process-table', 'data'),
    [Input('process-interval-component', 'n_intervals')]
)
def update_process_table(n):
    processes = get_process_info()
    df = pd.DataFrame(processes)
    df = df[(df['cpu_percent'] != 0) | (df['memory_percent'] != 0)]
    df = df.sort_values(['cpu_percent', 'memory_percent'], ascending=[False, False])
    return df.to_dict('records')

if __name__ == '__main__':
    activity_tracker_thread = threading.Thread(target=track_idle_activity)
    activity_tracker_thread.daemon = True
    activity_tracker_thread.start()

    app.run_server(debug=True)
