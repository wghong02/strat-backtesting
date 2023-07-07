import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hello, Dash!"),
    html.Div("Dash: A web application framework for Python."),
])

if __name__ == '__main__':
    app.run_server(debug=True)