from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import polars as pl
import dash_ag_grid as dag
import plotly.graph_objects as go

sheet_id = "1Y3FdKIxFvYFFhQjTSnXBW9V4Ab6Ippf2GoehPe0I1vU"

df = pl.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

habit_totals_list = []
habit_totals_count_list = []
inverse_habit_totals_list = []

##loop ever dataframe columns to get count and sum of each columns
for c in df.columns[1:9]:
    print(c)
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
)

##assign values
pages_read_c = habit_totals_count_list[0]
days_coding_c = habit_totals_count_list[1]
days_blogging_c = habit_totals_count_list[2]
days_meditated_c = habit_totals_count_list[3]
jounal_entries_c = habit_totals_count_list[4]
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

fig_list = []
for c in df.columns[1:]:
    fig_c = go.Figure()
    fig_c.add_trace(go.Bar(x=df["date"], y=df[c]))
    fig_c.update_traces(marker_color="#335eff")
    fig_list.append(fig_c)

ex_fig = fig_list[5].update_traces(marker_color="#ff5733")
sl_fig = fig_list[6].update_traces(marker_color="#ff5733")
wk_fig = fig_list[7].update_traces(marker_color="#ff5733")

al_fig = fig_list[8].update_traces(marker_color="#1fb81d")
mt_fig = fig_list[9].update_traces(marker_color="#1fb81d")
sg_fig = fig_list[10].update_traces(marker_color="#1fb81d")

tab_pages = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(html.H3(f"Read {pages_read} pages in {pages_read_c} days")),
                dcc.Graph(figure=fig_list[0]),
            ]
        ),
    ]
)
tab_code = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(f"Coded {days_coding} out of {days_coding_c} days")
                ),
                dcc.Graph(figure=fig_list[1]),
            ]
        ),
    ]
)
tab_blog = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(f"Blogged {days_blogging} out of {days_blogging_c} days")
                ),
                dcc.Graph(figure=fig_list[2]),
            ]
        ),
    ]
)
tab_med = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(
                        f"Meditated {days_meditated} out of {days_meditated_c} days"
                    )
                ),
                dcc.Graph(figure=fig_list[3]),
            ]
        ),
    ]
)
tab_jnl = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(
                        f"{jounal_entries} Jounal Entries out of {jounal_entries_c} days"
                    )
                ),
                dcc.Graph(figure=fig_list[4]),
            ]
        ),
    ]
)
tab_ex = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(
                        f"{minutes_exercised} Minutes exercised in {minutes_exercised_c} days"
                    )
                ),
                dcc.Graph(figure=ex_fig),
            ]
        ),
    ]
)
tab_slp = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(
                    html.H3(f"Days slept before 22h00: {days_slept_before_22h00}")
                ),
                dcc.Graph(figure=fig_list[6]),
            ]
        ),
    ]
)
tab_wake = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(html.H3(f"Days woke up at 05h00 : {days_woke_up_05h00}")),
                dcc.Graph(figure=fig_list[7]),
            ]
        ),
    ]
)
tab_alc = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(html.H3(f"Alcohol free days : {days_alcohol_free}")),
                dcc.Graph(figure=fig_list[8]),
            ]
        ),
    ]
)
tab_meat = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(html.H3(f"Days without meat : {days_without_meat}")),
                dcc.Graph(figure=fig_list[9]),
            ]
        ),
    ]
)
tab_sug = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Center(html.H3(f"Sugar free days : {days_without_sugar}")),
                dcc.Graph(figure=fig_list[10]),
            ]
        ),
    ]
)


tabs = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(tab_pages, label="Reading", label_style={"color": "#335eff"}),
                dbc.Tab(tab_code, label="Coding", label_style={"color": "#335eff"}),
                dbc.Tab(tab_blog, label="Blogging", label_style={"color": "#335eff"}),
                dbc.Tab(tab_med, label="Meditation", label_style={"color": "#335eff"}),
                dbc.Tab(tab_jnl, label="Jounaling", label_style={"color": "#335eff"}),
                dbc.Tab(tab_ex, label="Exersicing", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_slp, label="Sleep", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_wake, label="Wake up", label_style={"color": "#ff5733"}),
                dbc.Tab(tab_alc, label="Alcohol", label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_meat, label="Meat", label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_sug, label="Sugar", label_style={"color": "#1fb81d"}),
            ]
        )
    ]
)

##app styles
stylesheet = [dbc.themes.SKETCHY]
app = Dash(__name__, external_stylesheets=stylesheet)

##app layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                html.Br(),
                html.Center(html.H1("Live Habit tracker")),
            ]
        ),
        dbc.Row(
            [
                html.Center([tabs]),
            ]
        ),
        dbc.Row(
            [
                table,
            ]
        ),
    ]
)

##run app
if __name__ == "__main__":
    app.run(debug=True)
