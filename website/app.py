import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample data
df = px.data.gapminder()

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1("My Dashboard"),
    dcc.Graph(id='graph-1'),
    dcc.Graph(id='graph-2'),
    dcc.Graph(id='graph-3'),
    dcc.Graph(id='graph-4'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Life Expectancy vs GDP', 'value': 'lifeExp-gdpPercap'},
            {'label': 'Population vs GDP', 'value': 'pop-gdpPercap'}
        ],
        value='lifeExp-gdpPercap'
    )
])

# Define the callbacks
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure'),
     Output('graph-4', 'figure')],
    [Input('dropdown', 'value')]
)
def update_graphs(selected_value):
    if selected_value == 'lifeExp-gdpPercap':
        fig1 = px.scatter(df, x='gdpPercap', y='lifeExp', color='continent', 
                          title='Life Expectancy vs GDP Per Capita')
        fig2 = px.line(df, x='year', y='lifeExp', color='continent', 
                       title='Life Expectancy Over Time')
        fig3 = px.bar(df, x='continent', y='lifeExp', title='Average Life Expectancy by Continent')
        fig4 = px.box(df, x='continent', y='lifeExp', title='Life Expectancy Distribution by Continent')
    elif selected_value == 'pop-gdpPercap':
        fig1 = px.scatter(df, x='gdpPercap', y='pop', color='continent', 
                          title='Population vs GDP Per Capita')
        fig2 = px.line(df, x='year', y='pop', color='continent', 
                       title='Population Over Time')
        fig3 = px.bar(df, x='continent', y='pop', title='Total Population by Continent')
        fig4 = px.box(df, x='continent', y='pop', title='Population Distribution by Continent')

    return fig1, fig2, fig3, fig4

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
