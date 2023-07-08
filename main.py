import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
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
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div(id='content', style={'width': '80%', 'display': 'inline-block'})
])

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
            return [
                html.Button('Add New Strategy', id='add-strategy', n_clicks=0),
                html.Div(id='strategy-content')
            ]
        else:
            return f"You selected {button_id}"

@app.callback(
    Output('strategy-content', 'children'),
    [Input('add-strategy', 'n_clicks')]
)
def add_strategy(n_clicks):
    if n_clicks > 0:
        return [
            html.Div([
                html.Div('Gain', style={'color': 'green'}),
                dcc.Input(id='input-gain', type='number', value=0),
                html.Button('+ Gain', id='btn-gain', n_clicks=0)
            ]),
            html.Div([
                html.Div('Loss', style={'color': 'red'}),
                dcc.Input(id='input-loss', type='number', value=0),
                html.Button('- Loss', id='btn-loss', n_clicks=0)
            ]),
            html.Div(id='pnl', children='PnL: 0')
        ]
    
@app.callback(
    Output('pnl', 'children'),
    [Input('btn-gain', 'n_clicks'),
     Input('btn-loss', 'n_clicks')],
    [State('input-gain', 'value'),
     State('input-loss', 'value'),
     State('pnl', 'children')]
)
def update_pnl(n_clicks_gain, n_clicks_loss, gain, loss, pnl):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "PnL: 0"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        current_pnl = int(pnl.split(': ')[1])
        if button_id == 'btn-gain':
            return f"PnL: {current_pnl + gain}"
        elif button_id == 'btn-loss':
            return f"PnL: {current_pnl - loss}"


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)