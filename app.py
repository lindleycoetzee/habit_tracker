import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import polars as pl
import dash_ag_grid as dag
import plotly.graph_objects as go
import base64

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags=[{"name":"viewport",
                            "content": "width=device-width,initial-scale=1.0"}])

app.title = 'Live Habit Tracker'

server = app.server

sheet_id = "1Y3FdKIxFvYFFhQjTSnXBW9V4Ab6Ippf2GoehPe0I1vU"

df = pl.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

habit_totals_list = []
habit_totals_count_list = []
inverse_habit_totals_list = []

##loop ever dataframe columns to get count and sum of each columns
for c in df.columns[1:9]:
    count_df = df.select(pl.col(c).count())
    count_v = count_df[c][0]
    sum_df = df.select(pl.col(c)).sum()
    v = sum_df[c][0]
    habit_totals_count_list.append(count_v)
    habit_totals_list.append(v)

for c in df.columns[9:]:
    count_df = df.select(pl.col(c).count())
    sum_df = df.select(pl.col(c)).sum()
    count = count_df[c][0]
    sum = sum_df[c][0]
    v = count - sum
    inverse_habit_totals_list.append(v)

##create a table
table = dag.AgGrid(
    columnDefs=[{"field": c} for c in df.columns],
    rowData=df.to_dicts(),
    columnSize="sizeToFit",
    style={"backgroundColor": "#0074D9", "color": "white", "height": 270},
    dashGridOptions={"rowHeight": 30},
)

##assign values
pages_read_c = habit_totals_count_list[0]
days_coding_c = habit_totals_count_list[1]
days_blogging_c = habit_totals_count_list[2]
days_meditated_c = habit_totals_count_list[3]
journal_entries_c = habit_totals_count_list[4]
minutes_exercised_c = habit_totals_count_list[5]
days_slept_before_22h00_c = habit_totals_count_list[6]
days_woke_up_05h00_c = habit_totals_count_list[7]

pages_read = habit_totals_list[0]
days_coding = habit_totals_list[1]
days_blogging = habit_totals_list[2]
days_meditated = habit_totals_list[3]
jounal_entries = habit_totals_list[4]
minutes_exercised = habit_totals_list[5]
days_slept_before_22h00 = habit_totals_list[6]
days_woke_up_05h00 = habit_totals_list[7]

days_alcohol_free = inverse_habit_totals_list[0]
days_without_meat = inverse_habit_totals_list[1]
days_without_sugar = inverse_habit_totals_list[2]

date_list = df["date"].to_list()  # Convert the 'date' column to a list of strings

from statistics import mean

# Function to calculate the moving average for a given series of data
def moving_average(data, window_size=15):
    moving_averages = []
    for i in range(len(data) - window_size + 1):
        window = data[i : i + window_size]
        window = [x if x is not None else 0 for x in window]  # Replace None with 0
        moving_averages.append(mean(window))
    return moving_averages

fig_list = []
for c in df.columns[1:]:
    fig_c = go.Figure()
    y_values = df[c].to_list()  # Convert the Polars Series to a list of values
    moving_avg_15_values = moving_average(y_values)  # Calculate the 15-day moving average
    moving_avg_30_values = moving_average(y_values, window_size=30)  # Calculate the 30-day moving average

    # Add bar chart for original data
    fig_c.add_trace(go.Bar(x=date_list, y=y_values, name=c))

    # Add 15-day moving average line
    fig_c.add_trace(go.Scatter(x=date_list[14:], y=moving_avg_15_values, mode='lines',
                               name=f'{c} (15-day MA)', line=dict(color='black', width=2),
                               showlegend=True))

    # Add 30-day moving average line
    fig_c.add_trace(go.Scatter(x=date_list[29:], y=moving_avg_30_values, mode='lines',
                               name=f'{c} (30-day MA)', line=dict(color='grey', width=2),
                               showlegend=True))
    fig_c.update_layout(height=300)
    # Add other layout and formatting configurations as before
    if c == "pages read":
        fig_c.update_traces(marker_color="#335eff")
        fig_c.update_layout(
            title=f"Read {pages_read} pages in {pages_read_c} days at {round(pages_read/pages_read_c,2)} pages per day"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "code":
        fig_c.update_traces(marker_color="#335eff")
        fig_c.update_layout(
            title=f"Coded {days_coding} out of {days_coding_c} days = {round(days_coding/days_coding_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "blog":
        fig_c.update_traces(marker_color="#335eff")
        fig_c.update_layout(
            title=f"Blogged {days_blogging} out of {days_blogging_c} days = {round(days_blogging/days_blogging_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "meditation":
        fig_c.update_traces(marker_color="#335eff")
        fig_c.update_layout(
            title=f"Meditated {days_meditated} out of {days_meditated_c} days = {round(days_meditated/days_meditated_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "journal entry":
        fig_c.update_traces(marker_color="#335eff")
        fig_c.update_layout(
            title=f"{jounal_entries} Journal Entries out of {journal_entries_c} days = {round(jounal_entries/journal_entries_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "min excercise ":
        fig_c.update_traces(marker_color="#ff5733")
        fig_c.update_layout(
            title=f"{minutes_exercised} Minutes exercised in {minutes_exercised_c} days at {round(minutes_exercised/minutes_exercised_c,2)} minutes per day"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "in bed at 22:00":
        fig_c.update_traces(marker_color="#ff5733")
        fig_c.update_layout(
            title=f"Days slept before 22h00 : {days_slept_before_22h00} = {round(days_slept_before_22h00/days_slept_before_22h00_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "wake up at 05h00":
        fig_c.update_traces(marker_color="#ff5733")
        fig_c.update_layout(
            title=f"Days woke up at 05h00 : {days_woke_up_05h00} = {round(days_woke_up_05h00/days_woke_up_05h00_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "alcohol":
        fig_c.update_traces(marker_color="#1fb81d")
        fig_c.update_layout(
            title=f"Days without alcohol : {days_alcohol_free} = {round(days_alcohol_free/journal_entries_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "meat":
        fig_c.update_traces(marker_color="#1fb81d")
        fig_c.update_layout(
            title=f"Days without meat : {days_without_meat} = {round(days_without_meat/journal_entries_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    if c == "sugar":
        fig_c.update_traces(marker_color="#1fb81d")
        fig_c.update_layout(
            title=f"Days without sugar : {days_without_sugar} = {round(days_without_sugar/journal_entries_c * 100,2)}%"
        )
        fig_c.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                font=dict(family="Cabin Sketch, cursive", size=20, color="#000000"),
            ),
            font=dict(family="Comic Sans MS", size=12),
        )
    fig_list.append(fig_c)

tab_pages = dcc.Graph(figure=fig_list[0])
tab_code = dcc.Graph(figure=fig_list[1])
tab_blog = dcc.Graph(figure=fig_list[2])
tab_med = dcc.Graph(figure=fig_list[3])
tab_jnl = dcc.Graph(figure=fig_list[4])
tab_ex = dcc.Graph(figure=fig_list[5])
tab_slp = dcc.Graph(figure=fig_list[6])
tab_wake = dcc.Graph(figure=fig_list[7])
tab_alc = dcc.Graph(figure=fig_list[8])
tab_meat = dcc.Graph(figure=fig_list[9])
tab_sug = dcc.Graph(figure=fig_list[10])

tabs = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(tab_pages, label="Reading", label_style={"color": "#335eff"}),
                dbc.Tab(tab_code, label="Coding", label_style={"color": "#335eff"}),
                dbc.Tab(tab_blog, label="Blogging", label_style={"color": "#335eff"}),
                dbc.Tab(tab_med, label="Meditation", label_style={"color": "#335eff"}),
                dbc.Tab(tab_jnl, label="Journaling", label_style={"color": "#335eff"}),
                dbc.Tab(tab_ex, label="Exercising", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_slp, label="Sleep", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_wake, label="Wake up", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_alc, label="Alcohol", label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_meat, label="Meat", label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_sug, label="Sugar", label_style={"color": "#1fb81d"}),
            ]
        )
    ]
)

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

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row([
            html.Center(html.H1("Live Habit Tracker")),
        ]),
        dbc.Row([
            html.Center([tabs]),
        ]),
        dbc.Row([
            table,
        ]),
        html.Br(),
        footer,
        html.Link(rel="shortcut icon", href="website.png"),
    ], style={"overflow-x": "hidden"},
)



if __name__ == '__main__':
    app.run_server(debug=False)
