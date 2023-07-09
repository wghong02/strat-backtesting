import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import os

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True,
)

app.title = "Backtesting Tracker"

server = app.server

app.layout = html.Div([
    html.H1("Backtesting Tracker"),
    html.Div([
        html.Button('Home', id='option-1', n_clicks=0),
        html.Button('Strategies', id='option-2', n_clicks=0),
        html.Button('History', id='option-3', n_clicks=0),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div(id='content', style={'width': '80%', 'display': 'inline-block'}),
    dcc.Store(id='store', data={'pnl': 0, 'trades': 0, 'wins': 0})
])

# click on menu options
@app.callback(
    Output('content', 'children'),
    [Input('option-1', 'n_clicks'),
     Input('option-2', 'n_clicks'),
     Input('option-3', 'n_clicks')]
)

def update_content(option1, option2, option3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Select an option"
    else:
        option_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if option_id == 'option-2':
            return [
                html.Button('Add New Strategy', id='add-strategy', n_clicks=0),
                html.Div(id='strategy-content')
            ]
        else:
            return f"You selected {option_id}"

# to add new strategies
@app.callback(
    [Output('strategy-content', 'children'), Output('store', 'data')],
    [Input('add-strategy', 'n_clicks')]
)
def add_strategy(n_clicks):
    if n_clicks > 0:
        # Reset the CSV file
        pnl_history = pd.DataFrame({'PnL': [0]})
        pnl_history.to_csv('pnl_history.csv', index=False)
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
            html.Div(id='pnl', children='Total PnL: 0'),
            html.Div(id='winrate', children='Win Rate: 0%'),
            dcc.Graph(id='pnl-graph', config={'displayModeBar': True, 'scrollZoom': True})
        ], {'pnl': 0, 'trades': 0, 'wins': 0}


# update pnl    
@app.callback(
    [Output('pnl', 'children'), Output('pnl-graph', 'figure'), Output('store', 'data')],
    [Input('btn-gain', 'n_clicks'),
     Input('btn-loss', 'n_clicks')],
    [State('input-gain', 'value'),
     State('input-loss', 'value'),
     State('store', 'data')]
)

def update_pnl(n_clicks_gain, n_clicks_loss, gain, loss, data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "PnL: 0", {'data': [], 'layout': {'title': 'PnL over Time', 'xaxis': {'title': 'Number of Trades'}, 'yaxis': {'title': 'PnL', 'autorange': True}}}, data
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-gain':
            data['pnl'] += gain
            data['trades'] += 1
            data['wins'] += 1
        elif button_id == 'btn-loss':
            data['pnl'] -= loss
            data['trades'] += 1
        if os.path.exists('pnl_history.csv'):
            pnl_history = pd.read_csv('pnl_history.csv')
            new_row = pd.DataFrame({'PnL': [data['pnl']]})
            pnl_history = pd.concat([pnl_history, new_row], ignore_index=True)
        else:
            pnl_history = pd.DataFrame({'PnL': [data['pnl']]})
        pnl_history.to_csv('pnl_history.csv', index=False)
        return f"PnL: {data['pnl']}", {
            'data': [{'x': pnl_history.index, 'y': pnl_history['PnL'], 'type': 'scatter', 'mode': 'lines+markers'}],
            'layout': {'title': 'PnL over Time', 'xaxis': {'title': 'Number of Trades'}, 'yaxis': {'title': 'PnL', 'autorange': True}}
        }, data

# update winrate
@app.callback(
    Output('winrate', 'children'),
    [Input('store', 'data')],
)

def update_winrate(data):
    if data['trades'] == 0:
        return "Win Rate: 0%"
    else:
        winrate = (data['wins'] / data['trades']) * 100
        return f"Win Rate: {winrate:.2f}%"
    
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)