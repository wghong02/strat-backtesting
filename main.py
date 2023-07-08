import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "Backtesting Tracker"

server = app.server

app.layout = html.Div([
    html.H1("Backtesting Tracker"),
    html.Div([
        html.Button('Home', id='btn-1', n_clicks=0),
        html.Button('Strategies', id='btn-2', n_clicks=0),
        html.Button('History', id='btn-3', n_clicks=0),
    ], style={'width': '120%', 'display': 'inline-block'}),
    html.Div(id='content', style={'width': '80%', 'display': 'inline-block'})
])

import functions

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)