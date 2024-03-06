import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm
import base64


st.set_page_config(
        page_title="Fun",
        page_icon="🎆",
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

data_option = st.selectbox("Select from these dataframes :",
                     ("FULL","Without Mewtwo","Without Mewtwo and the KO's","Without the KO's"),
                     index=0, placeholder="Select the dataframe you'd like to use...")

if data_option == "FULL":
    data = pokedata.copy()  # If you want to use the full DataFrame
elif data_option == "Without Mewtwo":
    data = pokedata.iloc[1:].copy()  # Excluding the first row
elif data_option == "Without Mewtwo and the KO's":
    data = pokedata.iloc[1:-3].copy()  # Excluding the first row and the last three rows
elif data_option == "Without the KO's":
    data = pokedata.iloc[:-3].copy() 

pokebutton = st.checkbox('Display sprites on plot')

fig = go.Figure()

pokename_sorted = data.sort_values(by='LEN_POKEMON')
legend_labels = set()

# Your existing code for data preparation and scatter plot creation

# Fit linear regression
X = sm.add_constant(data['POSITION'])  # Add a constant to the predictor
model = sm.OLS(data['LEN_POKEMON'], X).fit()
const, slope = model.params

spearman_corr = pokename_sorted[['LEN_POKEMON', 'POSITION']].corr(method='spearman').iloc[0, 1]

for index, row in pokename_sorted.iterrows():
    number = row['NUMBER'] - 1
    sprite = pokesprites['SPRITE_NAME'].iloc[number]
    sprite_src = "/workspaces/pokedata-jroose11/static/" + sprite
    with open(sprite_src, "rb") as f:
        sprite_f = base64.b64encode(f.read()).decode("utf-8")
    value = row['LEN_POKEMON']
    dtypes = row['DTYPES']
    colordt_left = dt_type_pal_new_double.get(dtypes)[0]
    colordt_right = dt_type_pal_new_double.get(dtypes)[1]

    # Add scatter plot point
    scat_pos = go.Scatter(
        x=[row['POSITION']],
        y=[value],
        mode='markers',
        marker=dict(
            color=colordt_left,
            symbol='circle',
            size=10,
            line=dict(width=3, color=colordt_right)
        ),
        name=dtypes,
        text=row['POKEMON'] + '<br>' + dtypes,
        hoverinfo='text',
    )
    fig.add_trace(scat_pos)

    if pokebutton:
        # Add image overlay
        fig.add_layout_image(
            source='data:image/png;base64,' + sprite_f,
            x=row['POSITION'],
            y=value,
            xanchor="center",
            yanchor="middle",
            sizex=3,
            sizey=3,
            xref="x",
            yref="y"
        )
        
# Add linear regression line
fig.add_trace(go.Scatter(x=data['POSITION'], y=model.predict(), mode='lines', name='Linear Regression', line=dict(color='red')))

# Update layout
fig.update_layout(
    xaxis=dict(title='Position',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title='Length of Pokemon\'s names',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    legend=dict(title='Types'),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Scatter Plot of Pokemon Length vs. Position",
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

# Show plot
st.plotly_chart(fig)