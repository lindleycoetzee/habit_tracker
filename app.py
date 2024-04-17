import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags=[{"name":"viewport",
                            "content": "width=device-width,initial-scale=1.0"}])

app.title = 'Live Habit Tracker'

server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
