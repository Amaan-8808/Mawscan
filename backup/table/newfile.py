# import psutil
# import pandas as pd
# import dash
# from dash import dash_table
# from dash.dependencies import Input, Output

# # Create a Dash app
# app = dash.Dash(__name__)

# # Get process information
# processes = []
# for proc in psutil.process_iter(['name', 'username', 'cmdline', 'exe', 'memory_percent']):
#     try:
#         process_info = proc.info
#         process_info['cmdline'] = ' '.join(process_info['cmdline'])
#         processes.append(process_info)
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

# # Convert to a Pandas DataFrame
# df = pd.DataFrame(processes)

# # Create a Dash table
# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{'name': col, 'id': col} for col in df.columns],
#     data=df.to_dict('records'),
#     sort_action='native',  # Enable sorting
#     sort_mode='multi',  # Enable multi-column sorting
# )

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

# ! WORKING

# import psutil
# import pandas as pd
# import dash
# from dash import html, dash_table

# # Get process information
# processes = []
# for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
#     try:
#         process_info = proc.info
#         processes.append({
#             'name': process_info['name'],
#             'cpu_percent': process_info['cpu_percent'],
#             'memory_percent': process_info['memory_percent']
#         })
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

# # Create a Pandas DataFrame from the process information
# df = pd.DataFrame(processes)

# # Initialize the Dash app
# app = dash.Dash(__name__)

# # Define the app layout
# app.layout = html.Div([
#     html.H1('Process Information'),
#     dash_table.DataTable(
#         id='process-table',
#         columns=[{'name': col, 'id': col} for col in df.columns],
#         data=df.to_dict('records'),
#         style_cell={'textAlign': 'left'},
#         style_header={
#             'backgroundColor': 'rgb(230, 230, 230)',
#             'fontWeight': 'bold'
#         }
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

# ! reduced table size
import psutil
import pandas as pd
import dash
from dash import html, dash_table, dcc
from dash.dependencies import Output, Input

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

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1('Process Information'),
    dash_table.DataTable(
        id='process-table',
        columns=[{'name': 'Process Name', 'id': 'name'},
                 {'name': 'CPU Usage (%)', 'id': 'cpu_percent'},
                 {'name': 'Memory Usage (%)', 'id': 'memory_percent'}],
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll',
            'width': '50%'
        }
    ),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # 5 seconds in milliseconds
        n_intervals=0
    )
])

# Callback function to update the table data
@app.callback(Output('process-table', 'data'), Input('interval-component', 'n_intervals'))
def update_table(n):
    processes = get_process_info()
    df = pd.DataFrame(processes)
    # Filter out rows where both CPU and memory usage are zero
    df = df[(df['cpu_percent'] != 0) | (df['memory_percent'] != 0)]
    # Sort the DataFrame in descending order based on CPU and memory percent
    df = df.sort_values(['cpu_percent', 'memory_percent'], ascending=[False, False])
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)