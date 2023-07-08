import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

@app.callback(
    Output('content', 'children'),
    [Input('btn-1', 'n_clicks'),
    Input('btn-2', 'n_clicks'),
    Input('btn-3', 'n_clicks')]
)
def update_content(btn1, btn2, btn3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Select an option"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-2':
            return html.Button('Add New Strategy', id='add-strategy', n_clicks=0)
        else:
            return f"You selected {button_id}"

@app.callback(
    Output('add-strategy', 'children'),
    [Input('add-strategy', 'n_clicks')]
)
def add_strategy(n_clicks):
    if n_clicks > 0:
        return [
            html.Div([
                html.Div('Gain', style={'color': 'green'}),
                html.Button('+ Gain', id='btn-gain', n_clicks=0)
            ]),
            html.Div([
                html.Div('Loss', style={'color': 'red'}),
                html.Button('- Loss', id='btn-loss', n_clicks=0)
            ])
        ]