import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import statsmodels.api as sm

st.set_page_config(
        page_title="Moves",
        page_icon="💥",
        layout="wide"
    )

#palette

type_pal_old={"Dragon":"#4f60e2","Electrik":"#fac100","Fighting":"#ff8100","Fire":"#e72324","Ghost":"#713f71","Ground":"#92501b","Ice":"#3dd9ff","Insect":"#92a312","Normal":"#a0a3a0","Plant":"#3da324","Poison":"#923fcc","Psychic":"#ef3f7a","Rock":"#b1ab82","Water":"#2481ef","Fly":"#82baef"}
type_pal_new={"Dragon":"#036dc4","Electrik":"#f4d339","Fighting":"#cf3f6b","Fire":"#ff9e54","Ghost":"#5169ae","Ground":"#da7943","Ice":"#74cfc1","Insect":"#92c22b","Normal":"#929ba3","Plant":"#63bb5a","Poison":"#ac6bc9","Psychic":"#fa727a","Rock":"#c6b88d","Water":"#4f91d7","Fly":"#90abdf"}
dt_type_pal_new={"Dragon":"#036dc4","Dragon/Fly":["#036dc4","#90abdf"],"Electrik":"#f4d339","Electrik/Fly":["#f4d339","#90abdf"],"Fighting":"#cf3f6b","Fire":"#ff9e54","Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":"#da7943","Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":"#92c22b","Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":"#929ba3","Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":"#ac6bc9","Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":"#fa727a","Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":"#4f91d7","Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
dt_type_pal_new_double={"Dragon":["#036dc4","#036dc4"],"Dragon/Fly":["#036dc4","#90abdf"],"Electrik":["#f4d339","#f4d339"],"Electrik/Fly":["#f4d339","#90abdf"],"Fighting":["#cf3f6b","#cf3f6b"],"Fire":["#ff9e54","#ff9e54"],"Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":["#da7943","#da7943"],"Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":["#92c22b","#92c22b"],"Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":["#929ba3","#929ba3"],"Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":["#ac6bc9","#ac6bc9"],"Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":["#fa727a","#fa727a"],"Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":["#4f91d7","#4f91d7"],"Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
True_Tiers_palette={"SS":"#963634","S":"#ff7f7f","A":"#f79646","B":"#ffd467","C":"#ffff7f","D":"#bfff7f","E":"#7fff7f","F":"#7fffff","G":"#7f7fff","H":"#ff7fff","I":"#bf7fbf","J":"#60497a","KO":"#808080",}
Tiers_palette={1:"#963634",2:"#ff7f7f",3:"#f79646",4:"#ffd467",5:"#ffff7f",6:"#bfff7f",7:"#7fff7f",8:"#7fffff",9:"#7f7fff",10:"#ff7fff",11:"#bf7fbf",12:"#60497a",13:"#808080",}
Tiers_map={"SS":1,"S":2,"A":3,"B":4,"C":5,"D":6,"E":7,"F":8,"G":9,"H":10,"I":11,"J":12,"KO":13,}

#dataframe preparation

pokedata = pd.read_csv('./data/pokedata.csv', sep = ';')
pokemoves = pd.read_csv('./data/Full_Moves.csv', sep = ';')
att_moves = pd.read_csv('./data/FULL_ATT_MOVES.csv', sep = ';')
status_moves = pd.read_csv('./data/FULL_STATUS_MOVES.csv', sep = ';')


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
                     ("FULL","ONLY ATT MOVES"),
                     index=0, placeholder="Select the dataframe you'd like to use...")

if data_option == "FULL":
    data = pokemoves.copy()
elif data_option == "ONLY ATT MOVES":
    data = att_moves.copy()

Stats = st.radio("Choose the Stats you'd like to display :",
                         ["STRENGTH SUM", "MEAN STRENGTH", "MEDIAN STRENGTH", "PRECISION SUM", "MEAN PRECISION", "MEDIAN PRECISION","PP","MEAN PP","MEDIAN PP"],
                         horizontal=True)

Stats_without_prefixe = Stats.replace("MEAN ", "").replace("MEDIAN ","").replace(" SUM","")

moves_counts = data['TYPE'].value_counts()

fig = go.Figure()

pokemoves_ATT_sorted = data.sort_values(by='TYPE')

unique_move_type = pd.unique(pokemoves_ATT_sorted['TYPE'])
Stats_by_move_type = {}
mean_Stats_by_move_type = {}
median_Stats_by_move_type = {}

for move_type in unique_move_type:
    total_Stats = data.loc[data['TYPE'] == move_type, Stats_without_prefixe].sum()
    Stats_by_move_type[move_type] = total_Stats

for move_type in unique_move_type:
    mean_Stats = data.loc[data['TYPE'] == move_type, Stats_without_prefixe].mean()
    mean_Stats_by_move_type[move_type] = mean_Stats

for move_type in unique_move_type:
    median_Stats = data.loc[data['TYPE'] == move_type, Stats_without_prefixe].median()
    median_Stats_by_move_type[move_type] = median_Stats

sorted_Stats_by_move_type = {k: v for k, v in sorted(Stats_by_move_type.items())}
sorted_mean_Stats_by_move_type = {k: v for k, v in sorted(mean_Stats_by_move_type.items())}
sorted_median_Stats_by_move_type = {k: v for k, v in sorted(median_Stats_by_move_type.items())}

# Selecting data based on the chosen option for Stats
if Stats.startswith("MEAN"):
    Stats_values = list(sorted_mean_Stats_by_move_type.values())
    Stats_type_labels = list(sorted_mean_Stats_by_move_type.keys())
elif Stats.startswith("MEDIAN"):
    Stats_values = list(sorted_median_Stats_by_move_type.values())
    Stats_type_labels = list(sorted_median_Stats_by_move_type.keys())
else:
    Stats_values = list(sorted_Stats_by_move_type.values())
    Stats_type_labels = list(sorted_Stats_by_move_type.keys())

# Adding bar traces to the Plotly figure
sorted_df = pd.DataFrame({'Type': Stats_type_labels, 'Value': Stats_values}).sort_values(by='Value', ascending=False)

fig.add_trace(go.Bar(
    x=sorted_df['Type'],
    y=sorted_df['Value'],
    marker_color=[type_pal_new[label] for label in sorted_df['Type']],
    text=moves_counts[sorted_df['Type']],
    textposition='outside'))


# Updating layout
fig.update_layout(
    xaxis=dict(title="Move Type",
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title=Stats,
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': f"Pokemon {Stats} moves for each types",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100)
)

# Displaying the Plotly figure using Streamlit
st.plotly_chart(fig)
