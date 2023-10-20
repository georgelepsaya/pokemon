from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from extract_data import extract_data

URL = "https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/pokemon.csv"
df = extract_data(URL)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Pokémon Report', style={'textAlign': 'center'}),

    html.H2(children='Pokémon Ranking (from best to worst)'),

    html.H2(children='Pokémon Ranking (by strength against all others)'),

    html.H2(children='Pokémon Comparison'),

    html.Div([
        html.Label('Select First Pokémon:'),
        dcc.Dropdown(
            options=[{'label': f"{row['NAME']} (Gen {int(row['GENERATION'])})",
                      'value': f"{row['NAME']} {int(row['GENERATION'])}"}
                     for _, row in df[['NAME', 'GENERATION']].drop_duplicates().iterrows()],
            value='Bulbasaur 1',
            id='dropdown-selection-1'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Second Pokémon:'),
        dcc.Dropdown(
            options=[{'label': f"{row['NAME']} (Gen {int(row['GENERATION'])})", 'value': f"{row['NAME']} {int(row['GENERATION'])}"}
                     for _, row in df[['NAME', 'GENERATION']].drop_duplicates().iterrows()],
            value='Charmander 1',
            id='dropdown-selection-2'
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    html.H3('1. Overview Comparison', style={'margin-top': '20px'}),

    html.Div([
        html.Span('Total of '),
        html.Span(id="pokemon-1-name"),
        html.Span(': '),
        html.Span(id="pokemon-1-total")
    ], style={'margin-top': '20px'}),

    html.Div([
        html.Span('Total of '),
        html.Span(id="pokemon-2-name"),
        html.Span(': '),
        html.Span(id="pokemon-2-total")
    ]),

    dcc.Graph(id='graph-content'),

    html.H3('2. Battle Comparison', style={'margin-top': '20px'}),
], style={'font-family': "'Trebuchet MS', sans-serif", 'width': "80%", "margin": "0 auto"})


@app.callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection-1', 'value'),
     Input('dropdown-selection-2', 'value')]
)
def update_graph(pokemon1, pokemon2):
    # Fetch stats for both Pokemon
    values1 = pokemon1.split(' ')
    values2 = pokemon2.split(' ')
    stats1 = df[(df.NAME == " ".join(values1[:-1])) & (df.GENERATION == int(values1[-1]))].iloc[0]
    stats2 = df[(df.NAME == " ".join(values2[:-1])) & (df.GENERATION == int(values2[-1]))].iloc[0]

    # List of stats to compare
    stat_names = ['HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPD']

    # Fetch the specific stats for each Pokemon
    stats1_values = [stats1[stat] for stat in stat_names]
    stats2_values = [stats2[stat] for stat in stat_names]

    # Create the figure
    fig = go.Figure()

    # Add data for each pokemon
    fig.add_trace(go.Bar(x=stat_names, y=stats1_values, name=pokemon1))
    fig.add_trace(go.Bar(x=stat_names, y=stats2_values, name=pokemon2))

    return fig


@app.callback(
    Output('pokemon-1-name', 'children'),
    Input('dropdown-selection-1', 'value')
)
def update_pokemon_1_name(pokemon1):
    return pokemon1


@app.callback(
    Output('pokemon-1-total', 'children'),
    Input('dropdown-selection-1', 'value')
)
def update_pokemon_1_total(pokemon1):
    values = pokemon1.split(' ')
    stats = df[(df.NAME == " ".join(values[:-1])) & (df.GENERATION == int(values[-1]))].iloc[0]
    return stats['TOTAL']


@app.callback(
    Output('pokemon-2-name', 'children'),
    Input('dropdown-selection-2', 'value')
)
def update_pokemon_2_name(pokemon2):
    return pokemon2


@app.callback(
    Output('pokemon-2-total', 'children'),
    Input('dropdown-selection-2', 'value')
)
def update_pokemon_1_total(pokemon2):
    values = pokemon2.split(' ')
    stats = df[(df.NAME == " ".join(values[:-1])) & (df.GENERATION == int(values[-1]))].iloc[0]
    return stats['TOTAL']


if __name__ == '__main__':
    app.run(debug=True)
