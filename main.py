import dash
from dash import dcc
from dash import html
import pandas as pd

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "Backtesting Tracker"

app.layout = html.Div([
    html.H1("Hello, Dash!"),
    html.Div("Dash: A web application framework for Python."),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8080)