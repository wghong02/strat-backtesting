import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Reset CSV file
def reset_csv_file():
    pnl_history = pd.DataFrame({'PnL': [0]})
    pnl_history.to_csv('pnl_history.csv', index=False)