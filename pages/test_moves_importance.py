import pandas as pd
import streamlit as st
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

st.set_page_config(
    page_title="Position",
    page_icon="🔝",
    layout="wide"
)

# Assuming you have the same data preparation steps as before...

pokedata = pd.read_csv('/workspaces/pokedata-jroose11/data/pokedata.csv', sep=';')
pokemoves = pd.read_csv('/workspaces/pokedata-jroose11/data/Full_Moves.csv', sep=';')
att_moves = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_ATT_MOVES.csv', sep=';')
status_moves = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_STATUS_MOVES.csv', sep=';')
pokesprites = pd.read_csv('/workspaces/pokedata-jroose11/data/sprites_name.csv')

replace_values = {'int64': 0, 'float64': 0.0, 'object': ''}

for column in pokedata.columns:
    pokedata[column].fillna(replace_values.get(str(pokedata[column].dtype), ''), inplace=True)

for column in pokemoves.columns:
    pokemoves[column].fillna(replace_values.get(str(pokemoves[column].dtype), ''), inplace=True)

for column in att_moves.columns:
    att_moves[column].fillna(replace_values.get(str(att_moves[column].dtype), ''), inplace=True)

for column in status_moves.columns:
    status_moves[column].fillna(replace_values.get(str(status_moves[column].dtype), ''), inplace=True)

Tiers_palette={
                "SS":"#963634",
                "S":"#ff7f7f",
                "A":"#f79646",
                "B":"#ffd467",
                "C":"#ffff7f",
                "D":"#bfff7f",
                "E":"#7fff7f",
                "F":"#7fff7f",
                "G":"#7fffff",
                "H":"#7f7fff",
                "I":"#ff7fff",
                "J":"#bf7fbf",
                "K":"#60497a",
                "KO":"#808080",
               }

plot = go.Figure()

for tier, color in Tiers_palette.items():
    subset_data = pokedata[pokedata['TRUE_TIERS'] == tier]
    plot.add_trace(go.Violin(x=subset_data['TRUE_TIERS'],
                             y=subset_data['SUM_TM_MOVES'],
                             line_color='black',
                             fillcolor=color,
                             box_visible=True,
                             meanline_visible=True,
                             name=tier,
                             points='all',
                             marker=dict(color=color)))

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
)


st.plotly_chart(plot)
