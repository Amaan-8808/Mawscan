import dash
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from collections import deque
import random
import datetime
from dash import dcc

# Assuming you have a function that fetches CPU utilization
def get_cpu_utilization():
    # Replace with your actual method to fetch CPU utilization
    return random.randint(1, 100)

# Initialize deque with fixed size to store time and CPU utilization data
max_length = 50
times = deque(maxlen=max_length)
cpu_utilizations = deque(maxlen=max_length)

# Initialize the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Live CPU Utilization"),
    dcc.Graph(id='live-cpu-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # in milliseconds
        n_intervals=0
    ),
])

# Define the callback to update the graph
@app.callback(
    Output('live-cpu-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    times.append(datetime.datetime.now())
    cpu_utilizations.append(get_cpu_utilization())

    data = go.Scatter(
        x=list(times),
        y=list(cpu_utilizations),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data], 'layout': go.Layout(
        xaxis=dict(range=[min(times), max(times)]),
        yaxis=dict(range=[min(cpu_utilizations), max(cpu_utilizations)], title='CPU Utilization (%)'),
        title='Time Series'
    )}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
