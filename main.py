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
    dcc.Store(id='store-add', data={'pnl': 0, 'trades': 0, 'wins': 0}),
    dcc.Store(id='store-update', data={'pnl': 0, 'trades': 0, 'wins': 0}),
    dcc.ConfirmDialog(
        id='error-message',
        message='Gain must be greater than 0 and Loss must be non-negative.',
    ),
], className='default')

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
valid_gains = 0
valid_losses = 0

@app.callback(
    Output('strategy-content', 'children'),
    [Input('add-strategy', 'n_clicks')]
)
def add_strategy(n_clicks):
    global valid_gains, valid_losses  # use the global variables
    if n_clicks > 0:
        valid_gains = 0  # reset valid_gains
        valid_losses = 0  # reset valid_losses
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
            html.Div(id='pnl', children='PnL: 0'),
            html.Div(id='winrate', children='Win Rate: 0%'),
            dcc.Graph(id='pnl-graph', config={'displayModeBar': True, 'scrollZoom': True})
        ]


# update pnl and wr

@app.callback(
    [Output('pnl', 'children'), Output('pnl-graph', 'figure'), Output('winrate', 'children')],
    [Input('btn-gain', 'n_clicks'),
     Input('btn-loss', 'n_clicks')],
    [State('input-gain', 'value'),
     State('input-loss', 'value'),
     State('pnl', 'children'),
     State('winrate', 'children'),
     State('pnl-graph', 'figure')]
)
def update_pnl_and_winrate(n_clicks_gain, n_clicks_loss, gain, loss, pnl, winrate, figure):
    global valid_gains, valid_losses  # use the global variables
    ctx = dash.callback_context
    if not ctx.triggered:
        pnl_history = pd.DataFrame({'PnL': [0]})
        pnl_history.to_csv('pnl_history.csv', index=False)
        return "PnL: 0", {'data': [], 'layout': {'title': 'PnL over Time', 'xaxis': {'title': 'Number of Trades'}, 'yaxis': {'title': 'PnL', 'autorange': True}}}, "Win Rate: 0%"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        current_pnl = int(pnl.split(': ')[1])
        if button_id == 'btn-gain':
            if gain <= 0:
                return pnl, figure, winrate
            new_pnl = current_pnl + gain
            valid_gains += 1  # increment valid_gains
        elif button_id == 'btn-loss':
            if loss < 0:
                return pnl, figure, winrate
            new_pnl = current_pnl - loss
            valid_losses += 1  # increment valid_losses
        if os.path.exists('pnl_history.csv'):
            pnl_history = pd.read_csv('pnl_history.csv')
            new_row = pd.DataFrame({'PnL': [new_pnl]})
            pnl_history = pd.concat([pnl_history, new_row], ignore_index=True)
        else:
            pnl_history = pd.DataFrame({'PnL': [new_pnl]})
        pnl_history.to_csv('pnl_history.csv', index=False)
        
        total_trades = valid_gains + valid_losses  # use valid_gains and valid_losses
        wins = valid_gains
        winrate = (wins / total_trades) * 100 if total_trades > 0 else 0  # handle division by zero

        return f"PnL: {new_pnl}", {
            'data': [{'x': pnl_history.index, 'y': pnl_history['PnL'], 'type': 'scatter', 'mode': 'lines+markers'}],
            'layout': {'title': 'PnL over Time', 'xaxis': {'title': 'Number of Trades'}, 'yaxis': {'title': 'PnL', 'autorange': True}}
        }, f"Win Rate: {winrate:.2f}%"
# error message
@app.callback(
    Output('error-message', 'displayed'),
    [Input('btn-gain', 'n_clicks'),
     Input('btn-loss', 'n_clicks')],
    [State('input-gain', 'value'),
     State('input-loss', 'value')]
)
def display_error_message(n_clicks_gain, n_clicks_loss, gain, loss):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-gain' and n_clicks_gain > 0 and gain <= 0:
            return True
        elif button_id == 'btn-loss' and n_clicks_loss > 0 and loss < 0:
            return True
        else:
            return False

    
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)