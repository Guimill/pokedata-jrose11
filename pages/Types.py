import plotly.graph_objects as go
import pandas as pd
import streamlit as st

st.set_page_config(
        page_title="Types",
        page_icon="💧",
    )

#palette

type_pal_old={"Dragon":"#4f60e2","Electrik":"#fac100","Fighting":"#ff8100","Fire":"#e72324","Ghost":"#713f71","Ground":"#92501b","Ice":"#3dd9ff","Insect":"#92a312","Normal":"#a0a3a0","Plant":"#3da324","Poison":"#923fcc","Psychic":"#ef3f7a","Rock":"#b1ab82","Water":"#2481ef","Fly":"#82baef"}
type_pal_new={"Dragon":"#036dc4","Electrik":"#f4d339","Fighting":"#cf3f6b","Fire":"#ff9e54","Ghost":"#5169ae","Ground":"#da7943","Ice":"#74cfc1","Insect":"#92c22b","Normal":"#929ba3","Plant":"#63bb5a","Poison":"#ac6bc9","Psychic":"#fa727a","Rock":"#c6b88d","Water":"#4f91d7","Fly":"#90abdf"}
dt_type_pal_new={"Dragon":"#036dc4","Dragon/Fly":["#036dc4","#90abdf"],"Electrik":"#f4d339","Electrik/Fly":["#f4d339","#90abdf"],"Fighting":"#cf3f6b","Fire":"#ff9e54","Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":"#da7943","Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":"#92c22b","Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":"#929ba3","Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":"#ac6bc9","Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":"#fa727a","Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":"#4f91d7","Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
dt_type_pal_new_double={"Dragon":["#036dc4","#036dc4"],"Dragon/Fly":["#036dc4","#90abdf"],"Electrik":["#f4d339","#f4d339"],"Electrik/Fly":["#f4d339","#90abdf"],"Fighting":["#cf3f6b","#cf3f6b"],"Fire":["#ff9e54","#ff9e54"],"Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":["#da7943","#da7943"],"Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":["#92c22b","#92c22b"],"Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":["#929ba3","#929ba3"],"Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":["#ac6bc9","#ac6bc9"],"Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":["#fa727a","#fa727a"],"Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":["#4f91d7","#4f91d7"],"Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}

#dataframe preparation

pokedata = pd.read_csv('/workspaces/pokedata-jroose11/data/pokedata.csv', sep = ';')
pokemoves = pd.read_csv('/workspaces/pokedata-jroose11/data/Full_Moves.csv', sep = ';')
att_moves = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_ATT_MOVES.csv', sep = ';')
status_moves = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_STATUS_MOVES.csv', sep = ';')


replace_values = {'int64': 0, 'float64': 0.0, 'object': ''}

for column in pokedata.columns:
    pokedata[column].fillna(replace_values.get(str(pokedata[column].dtype), ''), inplace=True)

for column in pokemoves.columns:
    pokemoves[column].fillna(replace_values.get(str(pokemoves[column].dtype), ''), inplace=True)

for column in att_moves.columns:
    att_moves[column].fillna(replace_values.get(str(att_moves[column].dtype), ''), inplace=True)

for column in status_moves.columns:
    status_moves[column].fillna(replace_values.get(str(status_moves[column].dtype), ''), inplace=True)


#Stat preparation

# Grouping by DTYPES and calculating mean of HP
HP = pokedata.groupby('DTYPES')['HP'].mean().sort_values()
HP_2 = HP / 2

# Grouping by DTYPES and calculating mean of ATT
ATT = pokedata.groupby('DTYPES')['ATT'].mean().sort_values()
ATT_2 = ATT / 2

# Grouping by DTYPES and calculating mean of DEF
DEF = pokedata.groupby('DTYPES')['DEF'].mean().sort_values()
DEF_2 = DEF / 2

# Grouping by DTYPES and calculating mean of SPD
SPD = pokedata.groupby('DTYPES')['SPD'].mean().sort_values()
SPD_2 = SPD / 2

# Grouping by DTYPES and calculating mean of SPE
SPE = pokedata.groupby('DTYPES')['SPE'].mean().sort_values()
SPE_2 = SPE / 2

# Grouping by DTYPES and calculating mean of TOT
TOT = pokedata.groupby('DTYPES')['TOT'].mean().sort_values()
TOT_2 = TOT / 2

# Grouping by DTYPES and calculating mean of BULK
BULK = pokedata.groupby('DTYPES')['BULK'].mean().sort_values()
BULK_2 = BULK / 2


#UI preparation

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","TOT","BULK"],
                     horizontal = True)

Stats_2 = Stats + '_2'

#Ploting

# Defining colors based on dt_type_pal_new_double palette
colors = {key: dt_type_pal_new_double.get(key, ['blue', 'green']) for key in locals()[Stats].index}

data = []

# Modify traces to include hoverinfo
for i, stat_value in enumerate([locals()[Stats].values, locals()[Stats_2].values]):
    trace = go.Bar(
        x=locals()[Stats].index,
        y=stat_value,
        marker=dict(color=[colors[key][i] for key in locals()[Stats].index], line=dict(color='rgba(0,0,0,0)')),
        showlegend=False,
        hoverinfo='text'  # Set hoverinfo to include text
    )
    # Extracting Pokémon data for hover text
    hover_text = []
    for dtype in locals()[Stats].index:
        pokemon_list = pokedata.loc[pokedata['DTYPES'] == dtype, 'POKEMON'].tolist()
        hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
    trace.hovertext = hover_text  # Assigning hover text to the trace
    data.append(trace)

layout = go.Layout(
    title=f'Total {Stats} for each Types in Jroose Tier List',
    title_x=0.25,
    xaxis=dict(
        title='DTYPES',
        tickangle=45,
        tickfont=dict(
            size=10
        )
    ),
    yaxis=dict(
        title=Stats
    ),
    barmode='overlay'
)

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)