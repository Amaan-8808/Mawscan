import psutil
import time
from datetime import datetime
from collections import deque
from threading import Thread, Lock
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# In-memory data structure to store the data
data = deque(maxlen=100)  # Store the last 100 data points
data_lock = Lock()

# Function to collect data
def collect_data():
    while True:
        connections = psutil.net_connections(kind='inet')
        connection_count = len(connections)
        timestamp = datetime.now().isoformat()
        with data_lock:
            data.append({'timestamp': timestamp, 'connection_count': connection_count})
        time.sleep(2)  # Collect data every 2 seconds

# Start the data collection in a background thread
data_thread = Thread(target=collect_data)
data_thread.daemon = True
data_thread.start()

# Dash layout
app.layout = html.Div([
    html.H1('Network Connections Over Time'),
    dcc.Graph(id='connections-graph'),
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(
    Output('connections-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    with data_lock:
        timestamps = [item['timestamp'] for item in data]
        connection_counts = [item['connection_count'] for item in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=connection_counts,
        mode='lines+markers'
    ))
    fig.update_layout(
        title='Network Connections Over Time',
        xaxis_title='Time',
        yaxis_title='Number of Connections'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
