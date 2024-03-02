import plotly.graph_objects as go
import pandas as pd
import streamlit as st

st.set_page_config(
        page_title="Types",
        page_icon="💧",
        layout="wide"
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

#UI preparation
    
data_option = st.selectbox("Select from these dataframes :",
                     ("FULL","Without Mewtwo","Without Mewtwo and the KO's","Without the KO's"),
                     index=0, placeholder="Select the dataframe you'd like to use...")

if data_option == "FULL":
    df = pokedata.copy()  # If you want to use the full DataFrame
elif data_option == "Without Mewtwo":
    df = pokedata.iloc[1:].copy()  # Excluding the first row
elif data_option == "Without Mewtwo and the KO's":
    df = pokedata.iloc[1:-3].copy()  # Excluding the first row and the last three rows
elif data_option == "Without the KO's":
    df = pokedata.iloc[:-3].copy()  # Excluding the last three rows

st.markdown("***")

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","TOT","BULK","LEVEL","POSITION","TIERS","TIME"],
                     horizontal = True)

st.markdown("***")

Stats_sum = df.groupby('DTYPES')[Stats].sum().sort_values()
Stats_mean = df.groupby('DTYPES')[Stats].mean().sort_values()
Stats_median = df.groupby('DTYPES')[Stats].median().sort_values()

Stats_sum_2 = Stats_sum / 2
Stats_mean_2 = Stats_mean / 2
Stats_median_2 = Stats_median / 2

colors = {key: dt_type_pal_new_double.get(key, ['blue', 'green']) for key in Stats_sum.index}

pokemon_counts = df['DTYPES'].value_counts()

data_sum = []
data_mean = []
data_median = []

# Adding text annotation to the first bar only
trace = go.Bar(
    x=Stats_sum.index,
    y=Stats_sum.values,
    marker=dict(color=[colors[key][0] for key in Stats_sum.index], line=dict(color='rgba(0,0,0,0)')),
    showlegend=False,
    hoverinfo='text',  # Set hoverinfo to include text
    text=pokemon_counts[Stats_sum.index],  # Add text annotation with Pokémon counts
    textposition='outside',  # Set position of text annotation
)
# Extracting Pokémon data for hover text
hover_text = []
for dtype in Stats_sum.index:
    pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
    hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
trace.hovertext = hover_text  # Assigning hover text to the trace
data_sum.append(trace)

# Adding other bars without text annotation
for i, Stats_sum_value in enumerate([Stats_sum_2.values[1:]]):
    trace = go.Bar(
        x=Stats_sum.index[1:],
        y=Stats_sum_value,
        marker=dict(color=[colors[key][i + 1] for key in Stats_sum.index[1:]], line=dict(color='rgba(0,0,0,0)')),
        showlegend=False,
        hoverinfo='text',  # Set hoverinfo to include text
    )
    # Extracting Pokémon data for hover text
    hover_text = []
    for dtype in Stats_sum.index[1:]:
        pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
        hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
    trace.hovertext = hover_text  # Assigning hover text to the trace
    data_sum.append(trace)

layout_sum = go.Layout(
    xaxis=dict(
        title='DTYPES',
        tickangle=45,
        tickfont=dict(size=15),
        titlefont=dict(size=25)),
    yaxis=dict(
        title=f'{Stats_sum.name}',
        tickfont=dict(size=25),
        titlefont=dict(size=25)),
    barmode='overlay',
    title={
        'text': f'Total {Stats_sum.name} for each Types in Jroose Tier List',
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
)

fig_sum = go.Figure(data=data_sum, layout=layout_sum)
st.plotly_chart(fig_sum)

st.markdown("***")

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","TOT","BULK","LEVEL","POSITION","TIERS","TIME"],
                     horizontal = True, key = 1)


Stats_sum = df.groupby('DTYPES')[Stats].sum().sort_values()
Stats_mean = df.groupby('DTYPES')[Stats].mean().sort_values()
Stats_median = df.groupby('DTYPES')[Stats].median().sort_values()

Stats_sum_2 = Stats_sum / 2
Stats_mean_2 = Stats_mean / 2
Stats_median_2 = Stats_median / 2

st.markdown("***")

# Adding text annotation to the first bar only
trace = go.Bar(
    x=Stats_mean.index,
    y=Stats_mean.values,
    marker=dict(color=[colors[key][0] for key in Stats_mean.index], line=dict(color='rgba(0,0,0,0)')),
    showlegend=False,
    hoverinfo='text',  # Set hoverinfo to include text
    text=pokemon_counts[Stats_mean.index],  # Add text annotation with Pokémon counts
    textposition='outside',  # Set position of text annotation
)
# Extracting Pokémon data for hover text
hover_text = []
for dtype in Stats_mean.index:
    pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
    hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
trace.hovertext = hover_text  # Assigning hover text to the trace
data_mean.append(trace)

# Adding other bars without text annotation
for i, Stats_mean_value in enumerate([Stats_mean_2.values[1:]]):
    trace = go.Bar(
        x=Stats_mean.index[1:],
        y=Stats_mean_value,
        marker=dict(color=[colors[key][i + 1] for key in Stats_mean.index[1:]], line=dict(color='rgba(0,0,0,0)')),
        showlegend=False,
        hoverinfo='text',  # Set hoverinfo to include text
    )
    # Extracting Pokémon data for hover text
    hover_text = []
    for dtype in Stats_mean.index[1:]:
        pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
        hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
    trace.hovertext = hover_text  # Assigning hover text to the trace
    data_mean.append(trace)

layout_mean = go.Layout(
    xaxis=dict(
        title='DTYPES',
        tickangle=45,
        tickfont=dict(size=15),
        titlefont=dict(size=25)),
    yaxis=dict(
        title=f'{Stats_mean.name}',
        tickfont=dict(size=25),
        titlefont=dict(size=25)),
    barmode='overlay',
    title={
        'text': f'Mean {Stats_mean.name} for each Types in Jroose Tier List',
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
)

fig_mean = go.Figure(data=data_mean, layout=layout_mean)
st.plotly_chart(fig_mean)

st.markdown("***")

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","TOT","BULK","LEVEL","POSITION","TIERS","TIME"],
                     horizontal = True, key = 2)


Stats_sum = df.groupby('DTYPES')[Stats].sum().sort_values()
Stats_mean = df.groupby('DTYPES')[Stats].mean().sort_values()
Stats_median = df.groupby('DTYPES')[Stats].median().sort_values()

Stats_sum_2 = Stats_sum / 2
Stats_mean_2 = Stats_mean / 2
Stats_median_2 = Stats_median / 2

st.markdown("***")

# Adding text annotation to the first bar only
trace = go.Bar(
    x=Stats_median.index,
    y=Stats_median.values,
    marker=dict(color=[colors[key][0] for key in Stats_median.index], line=dict(color='rgba(0,0,0,0)')),
    showlegend=False,
    hoverinfo='text',  # Set hoverinfo to include text
    text=pokemon_counts[Stats_median.index],  # Add text annotation with Pokémon counts
    textposition='outside',  # Set position of text annotation
)
# Extracting Pokémon data for hover text
hover_text = []
for dtype in Stats_median.index:
    pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
    hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
trace.hovertext = hover_text  # Assigning hover text to the trace
data_median.append(trace)

# Adding other bars without text annotation
for i, Stats_median_value in enumerate([Stats_median_2.values[1:]]):
    trace = go.Bar(
        x=Stats_median.index[1:],
        y=Stats_median_value,
        marker=dict(color=[colors[key][i + 1] for key in Stats_median.index[1:]], line=dict(color='rgba(0,0,0,0)')),
        showlegend=False,
        hoverinfo='text',  # Set hoverinfo to include text
    )
    # Extracting Pokémon data for hover text
    hover_text = []
    for dtype in Stats_median.index[1:]:
        pokemon_list = df.loc[df['DTYPES'] == dtype, 'POKEMON'].tolist()
        hover_text.append(f"{dtype}: {', '.join(pokemon_list)}")
    trace.hovertext = hover_text  # Assigning hover text to the trace
    data_median.append(trace)

layout_median = go.Layout(
    xaxis=dict(
        title='DTYPES',
        tickangle=45,
        tickfont=dict(size=15),
        titlefont=dict(size=25)),
    yaxis=dict(
        title=f'{Stats_median.name}',
        tickfont=dict(size=25),
        titlefont=dict(size=25)),
    barmode='overlay',
    title={
        'text': f'Median {Stats_median.name} for each Types in Jroose Tier List',
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
)

fig_median = go.Figure(data=data_median, layout=layout_median)
st.plotly_chart(fig_median)