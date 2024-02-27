import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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

labels_used = set()  # Set to keep track of used labels

# Filter DataFrame to keep only the lowest position Pokémon for each tier
lowest_position_pokemon = pokedata.sort_values('POSITION').groupby('TIERS').first()


fig, ax = plt.subplots(figsize=(12, 8))  # Specify the figure size here

# Iterate over each row in the filtered DataFrame
for index, row in lowest_position_pokemon.iterrows():
    pokemon = row['POKEMON']
    tier = index
    dtypes = row['DTYPES']
    position = row['POSITION']
    
    # Fetching color and markerfacecoloralt based on dtypes
    colordt, markerfacecoloraltdt = dt_type_pal_new_double.get(dtypes, ('black', 'white'))
    
    # Plotting the point
    if dtypes not in labels_used:
        plt.plot(position, tier, c=colordt, markerfacecoloralt=markerfacecoloraltdt,
                 marker='.', markeredgecolor='none', linestyle='', markersize=15, fillstyle='left', label=dtypes)
        labels_used.add(dtypes)
    else:
        plt.plot(position, tier, c=colordt, markerfacecoloralt=markerfacecoloraltdt,
                 marker='.', markeredgecolor='none', linestyle='', markersize=15, fillstyle='left')


# Adding labels and title
yticks = pd.unique(pokedata['TRUE_TIERS'])
yticks_num = pd.unique(pokedata['TIERS'])
yticks_mapped = zip(yticks_num, yticks)
yticks_mapping = {num: label for num, label in zip(yticks_num, yticks)}

ax.set_yticks(list(yticks_mapping.keys()))
ax.set_yticklabels(list(yticks_mapping.values()))

ax.set_xlabel('Position')
ax.set_ylabel('TIERS')
ax.set_title('Best type for each tiers')

# Show legend
ax.legend()

# Show plot
st.pyplot(fig)