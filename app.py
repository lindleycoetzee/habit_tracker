import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, callback
import pandas as pd
import plotly.graph_objects as go
import base64

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags=[{"name": "viewport", "content": "width=device-width,initial-scale=1.0"}])

app.title = 'Live Habit Tracker'

server = app.server

sheet_id = "1Y3FdKIxFvYFFhQjTSnXBW9V4Ab6Ippf2GoehPe0I1vU"

df= pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
df["date"] = pd.to_datetime(df["date"], format= "%m/%d/%Y")

dropdown_period = dcc.Dropdown(["Day", "Week", "Month"],
                             value= "Day",
                             id=  "drpdwn_per",
                             style={"width": "50%",})

dropdown_habit = dcc.Dropdown(options= [{"label" : habit, "value" : str(habit)} for habit in df.columns[1:]],
                             value= "sugar",
                             id=  "drpdwn_hbt",
                             style={"width": "50%",})

linked_in_image = "linkedIn.jpg"
encoded_linkedIn_image = base64.b64encode(open(linked_in_image, "rb").read())

twitter_in_image = "twitter.jpg"
encoded_twitter_image = base64.b64encode(open(twitter_in_image, "rb").read())

website_in_image = "website.jpg"
encoded_website_image = base64.b64encode(open(website_in_image, "rb").read())

kaggle_in_image = "kaggle.jpg"
encoded_kaggle_image = base64.b64encode(open(kaggle_in_image, "rb").read())

footer = html.Center(
    [
        html.Footer(
            [
                html.A(
                    href="https://lindleycoetzee.webflow.io/",
                    target="blank",
                    children=[
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                encoded_website_image.decode()
                            ),
                            style={"width": "40px"},
                        )
                    ],
                ),
                html.A(
                    href="https://www.kaggle.com/lindleylawrence",
                    target="blank",
                    children=[
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                encoded_kaggle_image.decode()
                            ),
                            style={"width": "43px"},
                        )
                    ],
                ),
                html.A(
                    href="https://www.linkedin.com/in/lindleycoetzee",
                    target="blank",
                    children=[
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                encoded_linkedIn_image.decode()
                            ),
                            style={"width": "50px"},
                        )
                    ],
                ),
                html.A(
                    href="https://www.twitter.com/lindleycoetzee",
                    target="blank",
                    children=[
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                encoded_twitter_image.decode()
                            ),
                            style={"width": "40px"},
                        )
                    ],
                ),
                html.B([html.P("Lindley Coetzee : Works in accounting 😀")]),
            ]
        ),
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("Live Habit Tracker", className='text-center text-primary mb-4'))),
        dbc.Row([
            dbc.Col([
                html.Center([dropdown_habit])]),
            dbc.Col([
                html.Center([dropdown_period])]),
                    ]),
        dbc.Row([
            dcc.Graph(id="drpdwn_chart"),
        ]),
        dbc.Row(footer),

    ],
    fluid=True
)

@callback(Output("drpdwn_chart", "figure"),
          Input("drpdwn_per", "value"),
          Input("drpdwn_hbt", "value"))
def update_chart(per, hbt):
    fig = go.Figure()
    fig.update_layout(title=f"{hbt} per {str.lower(per)}")
    fig.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            font=dict(family="Cabin Sketch, cursive", size=28, color="#000000"),
        ),
        font=dict(family="Comic Sans MS", size=16),
    )
    dff = df
    if per == "Day":
        fig.add_trace(go.Bar(x = dff["date"], y = dff[hbt]))
        return fig
    elif per == "Week":
        dff = dff.groupby(pd.Grouper(key="date", freq="W")).sum().reset_index()
        fig.add_trace(go.Bar(x = dff["date"], y = dff[hbt]))
        return fig
    elif per == "Month":
        dff = dff.groupby(pd.Grouper(key="date", freq="ME")).sum().reset_index()
        fig.add_trace(go.Bar(x = dff["date"], y = dff[hbt]))
        return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8052)
