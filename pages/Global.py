import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.io as pio
import numpy as np
import plotly.express as px

st.set_page_config(
        page_title="Global",
        page_icon="🌍",
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

labels_used = set()  # Set to keep track of used labels

# Filter DataFrame to keep only the lowest position Pokémon for each tier
lowest_position_pokemon = data.sort_values('POSITION').groupby('TIERS').first()


rank, ax = plt.subplots(figsize=(12, 8))  # Specify the figure size here

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
yticks = pd.unique(data['TRUE_TIERS'])
yticks_num = pd.unique(data['TIERS'])
yticks_mapped = zip(yticks_num, yticks)
yticks_mapping = {num: label for num, label in zip(yticks_num, yticks)}

ax.set_yticks(list(yticks_mapping.keys()))
ax.set_yticklabels(list(yticks_mapping.values()))

ax.set_xlabel('Position')
ax.set_ylabel('TIERS')
ax.set_title('Best type for each tiers')

# Show legend
ax.legend()

# Compute the correlation matrix
data_heatmap = data.loc[:, ['POSITION', 'TIERS', 'SUM_LS_MOVES', 'SUM_TM_MOVES', 'LEVEL', 'HP', 'ATT', 'DEF', 'SPD', 'SPE', 'BULK', 'TOT']]
data_heatmap = data_heatmap.replace(',', '.', regex=True)

# Compute the correlation matrix
corr_data = data_heatmap.astype(float).corr(method='spearman')

# Generate a mask for the upper triangle
mask_heatmap = np.triu(np.ones_like(corr_data, dtype=bool))

# Set up the matplotlib figure

fig_heatmap = px.imshow(
    corr_data.mask(mask_heatmap).values,
    x=corr_data.index,
    y=corr_data.columns,
    color_continuous_scale=px.colors.diverging.RdBu,
    zmin=-1,
    zmax=1,
)


fig_heatmap.update_layout(
    yaxis=dict(
        tickfont=dict(size=15)),
    xaxis=dict(
        tickfont=dict(size=15)),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Which stats are the most related to each others",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100)
)

# Show the figures
st.plotly_chart(fig_heatmap)

st.markdown("""How to read this plot :
            
        The test used here is a spearman test.
            
        The range of the score is -1 to 1.
            
        When the result is -1 it means that there is a negative correlation between both variables
            for exemple the more TOT stats a pokemon have, the less his position will be.

        When the result is 1 it means that there is a positive correlation between both variables
            for exemple the less leveled is a pokemon, the less his position will be.
            
        Finally a score around 0 means that there's no apparent correlation between the variables.
            """)

lowest_position_pokemon = data.sort_values('POSITION').groupby('TIERS').first()

st.dataframe(lowest_position_pokemon)