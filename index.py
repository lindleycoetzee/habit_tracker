from dash import Dash, html, dcc, dash_table, Output, Input
import dash_bootstrap_components as dbc
import polars as pl
import dash_ag_grid as dag
import plotly.graph_objects as go
from ht import create_ht
import base64
from app import app, server

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

server = app.server
app.config.suppress_callback_exceptions = True


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        html.Br(),
        footer,
        html.Link(rel="shortcut icon", href="website.png"),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/ht":
        return create_ht()
    else:
        return create_ht()


if __name__ == "__main__":
    app.run_server(debug=False)
