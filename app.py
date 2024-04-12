from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import polars as pl
import dash_ag_grid as dag

sheet_id = "1Y3FdKIxFvYFFhQjTSnXBW9V4Ab6Ippf2GoehPe0I1vU"

df = pl.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

habit_totals_list = []
inverse_habit_totals_list = []

for c in df.columns[1:6]+df.columns[9:12]:
    sum_df = df.select(pl.col(c)).sum()
    v = sum_df[c][0]
    habit_totals_list.append(v)

for c in df.columns[6:9]:
    count_df = df.select(pl.col(c).count())
    sum_df = df.select(pl.col(c)).sum()
    count = count_df[c][0]
    sum = sum_df[c][0]
    v = count - sum
    inverse_habit_totals_list.append(v)

table = dag.AgGrid(
    columnDefs = [{"field" : c} for c in df.columns] ,
    rowData = df.to_dicts(),
    columnSize="sizeToFit",
    )

pages_read = habit_totals_list[0]
minutes_exercised = habit_totals_list[1]
days_coding = habit_totals_list[2]
days_blogging = habit_totals_list[3]
days_meditated = habit_totals_list[4]
days_alcohol_free = inverse_habit_totals_list[0]
days_without_meat = inverse_habit_totals_list[1]
days_without_sugar = inverse_habit_totals_list[2]
jounal_entries = habit_totals_list[5]
days_slept_before_22h00 = habit_totals_list[6]
days_woke_up_05h00 = habit_totals_list[7]


tab_pages = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Pages read : {pages_read}")),
        ]),
    ])
tab_code = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days coding : {days_coding}")),
        ]),
    ])
tab_blog = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days blogging  : {days_blogging}")),
        ]),
    ])
tab_med = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days meditating : {days_meditated}")),
        ]),
    ])
tab_jnl = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Jounal Entries : {jounal_entries}")),
        ]),
    ])
tab_ex = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Minutes exercised : {minutes_exercised}")),
        ]),
    ])
tab_slp = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days slept before 22h00: {days_slept_before_22h00}")),
        ]),
    ])
tab_wake = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days woke up 05h00 : {days_woke_up_05h00}")),
        ]),
    ])
tab_alc = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Alcohol free days : {days_alcohol_free}")),
        ]),
    ])
tab_meat = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Days without meat : {days_without_meat}")),
        ]),
    ])
tab_sug = dbc.Card([
    dbc.CardBody([
        html.Center(html.H3(f"Sugar free days : {days_without_sugar}")),
        ]),
    ])


tabs = dbc.Container([
        dbc.Tabs(
            [
                dbc.Tab(tab_pages, label="Reading",label_style={"color": "#335eff"}),
                dbc.Tab(tab_code, label="Coding",label_style={"color": "#335eff"}),
                dbc.Tab(tab_blog, label="Blogging",label_style={"color": "#335eff"}),
                dbc.Tab(tab_med, label="Meditation",label_style={"color": "#335eff"}),
                dbc.Tab(tab_jnl, label="Jounaling",label_style={"color": "#335eff"}),
                dbc.Tab(tab_ex, label="Exersicing",label_style={"color": "#ff5733"}),
                dbc.Tab(tab_slp, label="Sleep",label_style={"color": "#ff5733"}),
                dbc.Tab(tab_wake, label="Wake up",label_style={"color": "#ff5733"}),
                dbc.Tab(tab_alc, label="Alcohol",label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_meat, label="Meat",label_style={"color": "#1fb81d"}),
                dbc.Tab(tab_sug, label="Sugar",label_style={"color": "#1fb81d"}),
            ]
        )
    ])

stylesheet = [dbc.themes.SKETCHY]
app = Dash(__name__, external_stylesheets = stylesheet)

##app layout
app.layout = html.Div([

    dbc.Row([
        html.Br(),
        html.Center(html.H1("Live Habit tracker")),
        ]),          
    dbc.Row([
        html.Center([
            tabs
            ]),
        ]),
    dbc.Row([
        table,
        ]),

   
    ])

if __name__ == "__main__":
    app.run(debug = True)
