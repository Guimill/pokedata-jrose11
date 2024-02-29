import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm



st.set_page_config(
        page_title="Position",
        page_icon="🔝",
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

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","BULK"],
                     horizontal = True)

data = []

pokepos_sorted = pokedata.sort_values(by=Stats)
legend_labels_pos = set()

X_pos = sm.add_constant(pokepos_sorted['POSITION'])  
model_pos = sm.OLS(pokepos_sorted[Stats], X_pos).fit()
const_pos, slope_pos = model_pos.params

spearman_corr = pokepos_sorted[['POSITION', Stats]].corr(method='spearman').iloc[0, 1]

fig_pos = go.Figure()

# Add scatter trace for each row
for index, row in pokepos_sorted.iterrows():
    value = row[Stats]
    dtypes = row['DTYPES']
    colordt_left = dt_type_pal_new_double.get(dtypes)[0]
    colordt_right = dt_type_pal_new_double.get(dtypes)[1]
    if dtypes not in legend_labels_pos:
        scat = go.Scatter(x=[row['POSITION']], y=[value], mode='markers', marker=dict(color=colordt_left, symbol='circle', size=10, line=dict(width=3, color=colordt_right)), name=dtypes)
        fig_pos.add_trace(scat)
        legend_labels_pos.add(dtypes)
    else:
        scat = go.Scatter(x=[row['POSITION']], y=[value], mode='markers', marker=dict(color=colordt_left, symbol='circle', size=10, line=dict(width=3, color=colordt_right)), showlegend=False)
        fig_pos.add_trace(scat)


regression_line = const_pos + slope_pos * pokepos_sorted['POSITION']
fig_pos.add_trace(go.Scatter(x=pokepos_sorted['POSITION'], y=regression_line, mode='lines', name='Linear Regression', line=dict(color='red')))

# Update layout
fig_pos.update_layout(
    xaxis=dict(title='Position',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title=Stats,
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    legend=dict(title='Types'),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Scatter Plot of Pokemon {Stats} vs. Position",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    annotations=[dict(
        text=f"Spearman Correlation: {spearman_corr * -100:.2f}%",
        x=0.95, y=0.95,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color="black", size=12),
        bgcolor="#19c37d", opacity=0.8
    )],
)

# Show plot
st.plotly_chart(fig_pos)

data = []

poketiers_sorted = pokedata.sort_values(by=Stats)
legend_labels_tiers = set()

X_Tiers = sm.add_constant(poketiers_sorted['TIERS'])  
model_tiers = sm.OLS(poketiers_sorted[Stats], X_Tiers).fit()
const_tiers, slope_tiers = model_tiers.params

spearman_corr = poketiers_sorted[['TIERS', Stats]].corr(method='spearman').iloc[0, 1]

fig_tiers = go.Figure()

# Add scatter trace for each row
for index, row in poketiers_sorted.iterrows():
    value = row[Stats]
    dtypes = row['DTYPES']
    colordt_left = dt_type_pal_new_double.get(dtypes)[0]
    colordt_right = dt_type_pal_new_double.get(dtypes)[1]
    if dtypes not in legend_labels_tiers:
        scat = go.Scatter(x=[row['TIERS']], y=[value], mode='markers', marker=dict(color=colordt_left, symbol='circle', size=10, line=dict(width=3, color=colordt_right)), name=dtypes)
        fig_tiers.add_trace(scat)
        legend_labels_tiers.add(dtypes)
    else:
        scat = go.Scatter(x=[row['TIERS']], y=[value], mode='markers', marker=dict(color=colordt_left, symbol='circle', size=10, line=dict(width=3, color=colordt_right)), showlegend=False)
        fig_tiers.add_trace(scat)


regression_line = const_tiers + slope_tiers * poketiers_sorted['TIERS']
fig_tiers.add_trace(go.Scatter(x=poketiers_sorted['TIERS'], y=regression_line, mode='lines', name='Linear Regression', line=dict(color='red')))

# Update layout
fig_tiers.update_layout(
    xaxis=dict(title="Tiers",
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title=Stats,
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    legend=dict(title='Types'),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Scatter Plot of Pokemon {Stats} vs. Tiers",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100),
    annotations=[dict(
        text=f"Spearman Correlation: {spearman_corr * -100:.2f}%",
        x=0.95, y=0.95,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color="black", size=12),
        bgcolor="#19c37d", opacity=0.8
    )],
)

# Show plot
st.plotly_chart(fig_tiers)