import pandas as pd
import streamlit as st
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Moves relation to pokedata",
    page_icon=":dagger_knife:",
    layout="wide"
)


type_pal_old={"Dragon":"#4f60e2","Electrik":"#fac100","Fighting":"#ff8100","Fire":"#e72324","Ghost":"#713f71","Ground":"#92501b","Ice":"#3dd9ff","Insect":"#92a312","Normal":"#a0a3a0","Plant":"#3da324","Poison":"#923fcc","Psychic":"#ef3f7a","Rock":"#b1ab82","Water":"#2481ef","Fly":"#82baef"}
type_pal_new={"Dragon":"#036dc4","Electrik":"#f4d339","Fighting":"#cf3f6b","Fire":"#ff9e54","Ghost":"#5169ae","Ground":"#da7943","Ice":"#74cfc1","Insect":"#92c22b","Normal":"#929ba3","Plant":"#63bb5a","Poison":"#ac6bc9","Psychic":"#fa727a","Rock":"#c6b88d","Water":"#4f91d7","Fly":"#90abdf"}
dt_type_pal_new={"Dragon":"#036dc4","Dragon/Fly":["#036dc4","#90abdf"],"Electrik":"#f4d339","Electrik/Fly":["#f4d339","#90abdf"],"Fighting":"#cf3f6b","Fire":"#ff9e54","Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":"#da7943","Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":"#92c22b","Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":"#929ba3","Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":"#ac6bc9","Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":"#fa727a","Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":"#4f91d7","Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
dt_type_pal_new_double={"Dragon":["#036dc4","#036dc4"],"Dragon/Fly":["#036dc4","#90abdf"],"Electrik":["#f4d339","#f4d339"],"Electrik/Fly":["#f4d339","#90abdf"],"Fighting":["#cf3f6b","#cf3f6b"],"Fire":["#ff9e54","#ff9e54"],"Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":["#da7943","#da7943"],"Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":["#92c22b","#92c22b"],"Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":["#929ba3","#929ba3"],"Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":["#ac6bc9","#ac6bc9"],"Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":["#fa727a","#fa727a"],"Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":["#4f91d7","#4f91d7"],"Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
True_Tiers_palette={"SS":"#963634","S":"#ff7f7f","A":"#f79646","B":"#ffd467","C":"#ffff7f","D":"#bfff7f","E":"#7fff7f","F":"#7fffff","G":"#7f7fff","H":"#ff7fff","I":"#bf7fbf","J":"#60497a","KO":"#808080",}
Tiers_palette={1:"#963634",2:"#ff7f7f",3:"#f79646",4:"#ffd467",5:"#ffff7f",6:"#bfff7f",7:"#7fff7f",8:"#7fffff",9:"#7f7fff",10:"#ff7fff",11:"#bf7fbf",12:"#60497a",13:"#808080",}
Tiers_map={"SS":1,"S":2,"A":3,"B":4,"C":5,"D":6,"E":7,"F":8,"G":9,"H":10,"I":11,"J":12,"KO":13,}


# Assuming you have the same data preparation steps as before...

pokedata = pd.read_csv('../data/pokedata.csv', sep=';')
pokemoves = pd.read_csv('../data/Full_Moves.csv', sep=';')
att_moves = pd.read_csv('../data/FULL_ATT_MOVES.csv', sep=';')
status_moves = pd.read_csv('../data/FULL_STATUS_MOVES.csv', sep=';')
pokesprites = pd.read_csv('../data/sprites_name.csv')

replace_values = {'int64': 0, 'float64': 0.0, 'object': ''}

for column in pokedata.columns:
    pokedata[column].fillna(replace_values.get(str(pokedata[column].dtype), ''), inplace=True)

for column in pokemoves.columns:
    pokemoves[column].fillna(replace_values.get(str(pokemoves[column].dtype), ''), inplace=True)

for column in att_moves.columns:
    att_moves[column].fillna(replace_values.get(str(att_moves[column].dtype), ''), inplace=True)

for column in status_moves.columns:
    status_moves[column].fillna(replace_values.get(str(status_moves[column].dtype), ''), inplace=True)

Moves = st.checkbox('Switch between LS / TM Moves analysis')

tiers = sm.add_constant(pokedata['TIERS'])

plot = go.Figure()

for tier, color in True_Tiers_palette.items():
    if Moves:
        moves = 'SUM_TM_MOVES'
    else:
        moves = 'SUM_LS_MOVES'
    model_tiers = sm.OLS(pokedata[moves], tiers).fit()
    const_tiers, slope_tiers = model_tiers.params
    spearman_corr = pokedata[['TIERS', moves]].corr(method='spearman').iloc[0, 1]

    subset_data = pokedata[pokedata['TRUE_TIERS'] == tier]
    plot.add_violin(x=subset_data['TRUE_TIERS'],
                             y=subset_data[moves],
                             line_color='black',
                             fillcolor=color,
                             box_visible=True,
                             meanline_visible=True,
                             name=tier,
                             points='all',
                             marker=dict(color=color))
    
regression_line_tiers = const_tiers + slope_tiers * pokedata['TIERS']
plot.add_trace(go.Scatter(x=pokedata['TRUE_TIERS'], y=regression_line_tiers, mode='lines', name='Linear Regression', line=dict(color='red')))

plot.update_layout(
    xaxis=dict(title='TIERS',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title='Sum of moves for each pokemon',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    legend=dict(title='Types'),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Number of TM moves disposable in each tier",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    annotations=[dict(
        text=f"Spearman Correlation: {spearman_corr * 100:.2f}%",
        x=1, y=1.05,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color="black", size=16),
        bgcolor="#f06d57", opacity=0.8
    )],
)


st.plotly_chart(plot)
