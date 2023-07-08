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
    html.H1("Hello, Dash!"),
    html.Div("Dash: A web application framework for Python."),
    html.Div([
        html.H3("Menu"),
        html.Button('Option 1', id='btn-1', n_clicks=0),
        html.Button('Option 2', id='btn-2', n_clicks=0),
        html.Button('Option 3', id='btn-3', n_clicks=0),
        html.Button('Option 4', id='btn-4', n_clicks=0),
        html.Button('Option 5', id='btn-5', n_clicks=0),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div(id='content', style={'width': '80%', 'display': 'inline-block'})
])

@app.callback(
    Output('content', 'children'),
    [Input('btn-1', 'n_clicks'),
     Input('btn-2', 'n_clicks'),
     Input('btn-3', 'n_clicks'),
     Input('btn-4', 'n_clicks'),
     Input('btn-5', 'n_clicks')]
)
def update_content(btn1, btn2, btn3, btn4, btn5):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Select an option"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return f"You selected {button_id}"

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)