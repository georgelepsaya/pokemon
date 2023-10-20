import pandas as pd
from dash import Dash, html, dcc, Output, Input, dash_table
from dash.dash_table.Format import Format
import plotly.graph_objects as go
import random
from scripts.extract_data import extract_data


type_chart = {
    "normal": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 0.5,
        "ghost": 0,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1
    },
    "fire": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 1,
        "grass": 2,
        "ice": 2,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 2,
        "rock": 0.5,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 2,
        "fairy": 1
    },
    "water": {
        "normal": 1,
        "fire": 2,
        "water": 0.5,
        "electric": 1,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 2,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 2,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 1,
        "fairy": 1
    },
    "electric": {
        "normal": 1,
        "fire": 1,
        "water": 2,
        "electric": 0.5,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 0,
        "flying": 2,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 1,
        "fairy": 1
    },
    "grass": {
        "normal": 1,
        "fire": 0.5,
        "water": 2,
        "electric": 1,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 0.5,
        "ground": 2,
        "flying": 0.5,
        "psychic": 1,
        "bug": 0.5,
        "rock": 2,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1
    },
    "ice": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 1,
        "grass": 2,
        "ice": 0.5,
        "fighting": 1,
        "poison": 1,
        "ground": 2,
        "flying": 2,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1
    },
    "fighting": {
        "normal": 2,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 2,
        "fighting": 1,
        "poison": 0.5,
        "ground": 1,
        "flying": 0.5,
        "psychic": 0.5,
        "bug": 0.5,
        "rock": 2,
        "ghost": 0,
        "dragon": 1,
        "dark": 2,
        "steel": 2,
        "fairy": 0.5
    },
    "poison": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 2,
        "ice": 1,
        "fighting": 1,
        "poison": 0.5,
        "ground": 0.5,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 0.5,
        "ghost": 0.5,
        "dragon": 1,
        "dark": 1,
        "steel": 0,
        "fairy": 2
    },
    "ground": {
        "normal": 1,
        "fire": 2,
        "water": 1,
        "electric": 2,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 2,
        "ground": 1,
        "flying": 0,
        "psychic": 1,
        "bug": 0.5,
        "rock": 2,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 2,
        "fairy": 1
    },
    "flying": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 0.5,
        "grass": 2,
        "ice": 1,
        "fighting": 2,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 2,
        "rock": 0.5,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1
    },
    "psychic": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 2,
        "poison": 2,
        "ground": 1,
        "flying": 1,
        "psychic": 0.5,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 1,
        "dark": 0,
        "steel": 0.5,
        "fairy": 1
    },
    "bug": {
        "normal": 1,
        "fire": 0.5,
        "water": 1,
        "electric": 1,
        "grass": 2,
        "ice": 1,
        "fighting": 0.5,
        "poison": 0.5,
        "ground": 1,
        "flying": 0.5,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 0.5,
        "dragon": 1,
        "dark": 2,
        "steel": 0.5,
        "fairy": 0.5
    },
    "rock": {
        "normal": 1,
        "fire": 2,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 2,
        "fighting": 0.5,
        "poison": 1,
        "ground": 0.5,
        "flying": 2,
        "psychic": 1,
        "bug": 2,
        "rock": 1,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1
    },
    "ghost": {
        "normal": 0,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 2,
        "dragon": 1,
        "dark": 0.5,
        "steel": 1,
        "fairy": 1
    },
    "dragon": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 1,
        "steel": 0.5,
        "fairy": 0
    },
    "dark": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 0.5,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 2,
        "dragon": 1,
        "dark": 0.5,
        "steel": 1,
        "fairy": 0.5
    },
    "steel": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 0.5,
        "grass": 1,
        "ice": 2,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 2
    },
    "fairy": {
        "normal": 1,
        "fire": 0.5,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 2,
        "poison": 0.5,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 2,
        "steel": 0.5,
        "fairy": 1
    }
}



URL = "https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/pokemon.csv"
df = extract_data(URL)

# DataFrame with pokemons ranked by types
ranked_by_types = pd.read_csv('data/ranked_by_type.csv', index_col=0)
ranked_by_types['Rank'] = ranked_by_types['strength'].rank(ascending=False, method='dense').astype(int)
ranked_by_types = ranked_by_types.sort_values('Rank')
cols = ['Rank', 'strength'] + [col for col in ranked_by_types.columns if col not in ['strength', 'Rank']]
ranked_by_types = ranked_by_types[cols]
ranked_by_types.rename(columns={'strength': 'Strength'}, inplace=True)

# DataFrame with pokemons ranked by scores
ranked_by_scores = pd.read_csv('data/ranked_by_scores.csv', index_col=0)
formatted_columns = []
for column_name in ranked_by_scores.columns:
    if column_name in ['Total Score', 'Max Score', 'Mean Score']:
        formatted_columns.append({"name": column_name, "id": column_name, "type": "numeric", "format": Format(precision=4)})
    else:
        formatted_columns.append({"name": column_name, "id": column_name})

# Initiate a Dash app
app = Dash(__name__)

# Define a Dash app layout
app.layout = html.Div([
    html.H1(children='Pokémon Report', style={'textAlign': 'center'}),

    html.H2(children='1. Pokémon Ranking (by comparing Stats)'),

    html.Div("This is a ranking done using formula:", style={'marginBottom': '10px'}),
    html.Div("""([Attack of attacking pokemon] - [Defense of defending pokemon])*0.8 + ([Sp. Attack of attacking 
    pokemon] - [Sp. Defense of defending pokemon])*0.2""", style={'fontStyle': 'italic', 'marginBottom': '10px'}),
    html.Div("Pokémon are ranked by a Total Score.", style={'marginBottom': '10px'}),

    dash_table.DataTable(
        id="rank_table_1",
        columns=formatted_columns,
        data=ranked_by_scores.to_dict('records'),
        style_table={'overflowX': 'scroll', 'padding': '5px'},
        style_cell={'width': '250px'},
        page_size=20,
        sort_action='native',
    ),

    html.H2(children='2. Pokémon Ranking (by Type Strength)'),
    html.Div("""This ranking is done based only on the strength of types of a pokemon.
    The strongest pokemon is the one with the biggest value of accumulated score of multipliers.""",
             style={'marginBottom': '10px'}),
    html.Div("Following this part of the documentation:", style={'marginBottom': '10px'}),
    html.Div("""If the enemy has two types, both are taken into account, and the multipliers for each Type are
             multiplied together. Thus, the full range of possible Type Modifier values is as follows: 4, 2, 1, 0.5, 
             0.25, 0.""", style={'fontStyle': 'italic', 'marginBottom': '10px'}),
    html.Div("To calculate the overall strength against others we will sum the Type Modifiers for every pokemon.",
             style={'marginBottom': '10px'}),

    dash_table.DataTable(
        id="rank_table_2",
        columns=[{"name": i, "id": i} for i in ranked_by_types.columns],
        data=ranked_by_types.to_dict('records'),
        style_table={'overflowX': 'scroll', 'padding': '5px'},
        style_cell={'width': '250px'},
        page_size=20,
        sort_action='native',
    ),

    html.H2(children='3. Pokémon Comparison'),

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

    html.H3('1) Overview Comparison', style={'margin-top': '20px'}),

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

    html.H3('2) Battle Comparison', style={'marginTop': '20px'}),
    html.Div("The formula we will use is to calculate the damage is following:"),
    html.Div("""((2A/5+2)*B*C)/D)/50)+2)*X)*Y/10)*Z)/255""", style={'fontStyle': 'italic', 'marginBottom': '10px'}),
    html.B("Explanation:", style={'display': 'block'}),
    html.Ol([
        html.Li("""Since we don't have data on specific moves pokemon make, we are going to assume that the type of a 
        move matches matches the type of the pokemon. Which is why we are going to take the most damaging type of an 
        attack for a type - Physical or Special."""),
        html.Li("""For the same reason we will assume that the type of an attack always matches the physical or
        special attack of the pokemon. Hence X is always 1.5 in our case."""),
        html.Li("""We will refer the Type Modifier chart used previously to determine the value of Y."""),
        html.Li("""Since we don't know the move, we will assign it to the flat values of 70."""),
        html.Li("""For a level, we will also simply take a constant value of 50."""),
        html.Li("""Damage will be a randomly generated number from 217 to 255, as stated in the documentation.""")
    ]),
    html.Div("""Despite all the assumptions due to the lack of move and level data, this model is still precise
    enough to estimate and compare damage based on the pokemon specific data."""),

    html.Div([
        html.Div([
            html.Div([
                html.Span("Damage of "),
                html.Span(id="1-pok-1-name"),
                html.Span(" to "),
                html.Span(id="1-pok-2-name")
            ], style={"fontWeight": "bold", "textAlign": "center"}),
            html.Div("390", id="damage-1")
        ], style={"width": "100%"}),
        html.Div([
            html.Div([
                html.Span("Damage of "),
                html.Span(id="2-pok-2-name"),
                html.Span(" to "),
                html.Span(id="2-pok-1-name")
            ], style={"fontWeight": "bold", "textAlign": "center"}),
            html.Div("390", id="damage-2")
        ], style={"width": "100%"})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '30px'}),

    html.Footer("Report prepared by Georgy Lepsaya", style={'marginTop': '150px', 'marginBottom': '40px', 'color': 'grey', 'textAlign':
                                         'center'})
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


@app.callback(
    [Output('1-pok-1-name', 'children'),
     Output('2-pok-1-name', 'children')],
    Input('dropdown-selection-1', 'value')
)
def update_pok_1_names(pokemon1):
    return pokemon1, pokemon1


@app.callback(
    [Output('1-pok-2-name', 'children'),
     Output('2-pok-2-name', 'children')],
    Input('dropdown-selection-2', 'value')
)
def update_pok_1_names(pokemon1):
    return pokemon1, pokemon1


@app.callback(
    [Output('damage-1', 'children'),
     Output('damage-2', 'children')],
    [Input('dropdown-selection-1', 'value'),
     Input('dropdown-selection-2', 'value')]
)
def update_damage(pokemon1, pokemon2):
    def calculate_damage(pok1, pok2):
        a = 50
        c = 70
        x = 1.5
        z = random.randint(217, 255)
        b = pok1['ATK']
        d = pok2['DEF']
        atk_type = 'physical'
        if pok1['ATK'] < pok1['SP_ATK']:
            b = pok1['SP_ATK']
            atk_type = 'special'
        if atk_type == 'special':
            d = pok2['SP_DEF']
        y = 0
        type1_pok1 = pok1['TYPE1'].lower()
        type1_pok2 = pok2['TYPE1'].lower()
        type2_pok1 = None if pd.isna(pok1['TYPE2']) else pok1['TYPE2'].lower()
        type2_pok2 = None if pd.isna(pok2['TYPE2']) else pok2['TYPE2'].lower()
        mult11 = type_chart[type1_pok1][type1_pok2]
        mult12 = 1 if type2_pok2 is None else type_chart[type1_pok1][type2_pok2]
        tm1 = mult11 * mult12
        if type2_pok1:
            mult21 = type_chart[type2_pok1][type1_pok2]
            mult22 = 1 if type2_pok2 is None else type_chart[type2_pok1][type2_pok2]
            tm2 = mult21 * mult22
            y = max(tm1, tm2)
        else:
            y = tm1
        damage = ((((((((2*a / 5 + 2)*b*c)/d)/50) + 2)*x)*y/10)*z)/255
        return damage

    values1 = pokemon1.split(' ')
    stats1 = df[(df.NAME == " ".join(values1[:-1])) & (df.GENERATION == int(values1[-1]))].iloc[0]

    values2 = pokemon2.split(' ')
    stats2 = df[(df.NAME == " ".join(values2[:-1])) & (df.GENERATION == int(values2[-1]))].iloc[0]

    return calculate_damage(stats1, stats2), calculate_damage(stats2, stats1)


if __name__ == '__main__':
    app.run(debug=True)
