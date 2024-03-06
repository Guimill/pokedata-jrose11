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

Moves = st.checkbox('Switch between LS / TM Moves analysis')

tiers = sm.add_constant(pokedata['TIERS'])

plot = go.Figure()

for tier, color in Tiers_palette.items():
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
