from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm
import base64

np.random.seed(556)

st.set_page_config(
        page_title="Prediction",
        page_icon="🌠",
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

pokedata = pd.read_csv('../data/pokedata.csv', sep = ';')
pokemoves = pd.read_csv('../data/Full_Moves.csv', sep = ';')
att_moves = pd.read_csv('../data/FULL_ATT_MOVES.csv', sep = ';')
status_moves = pd.read_csv('../data/FULL_STATUS_MOVES.csv', sep = ';')
pokesprites = pd.read_csv('../data/sprites_name.csv')
pokestats = pd.read_csv('../data/Full_pokestats.csv', sep = ';')

replace_values = {'int64': 0, 'float64': 0.0, 'object': ''}

for column in pokedata.columns:
    pokedata[column].fillna(replace_values.get(str(pokedata[column].dtype), ''), inplace=True)

for column in pokemoves.columns:
    pokemoves[column].fillna(replace_values.get(str(pokemoves[column].dtype), ''), inplace=True)

for column in att_moves.columns:
    att_moves[column].fillna(replace_values.get(str(att_moves[column].dtype), ''), inplace=True)

for column in status_moves.columns:
    status_moves[column].fillna(replace_values.get(str(status_moves[column].dtype), ''), inplace=True)

for column in pokestats.columns:
    pokestats[column].fillna(replace_values.get(str(pokestats[column].dtype), ''), inplace=True)

################################################## position #########################################################

Stats = st.radio("Choose the Stats you'd like to display :",
                     ["HP","ATT","DEF","SPD","SPE","BULK","NUMBER"],
                     horizontal = True)

pokebutton_pos = st.checkbox('Display sprites on plot')

pokepos_sorted = pokedata.sort_values(by=Stats)

pokestats_sorted = pokestats.sort_values(by=Stats)

model = RandomForestRegressor()  # You can try other models as well

# Step 5: Model Training
X_train = pokepos_sorted[[Stats]]  # Using the selected stat as the feature
y_train = pokepos_sorted['POSITION']  # Target variable
model.fit(X_train, y_train)

# Step 7: Prediction
# Assuming pokestats_sorted is a DataFrame containing the stats of the remaining Pokémon
X_test = pokestats_sorted[[Stats]]  # Using the selected stat as the feature
predicted_positions = model.predict(X_test)

# Transform predicted positions to 151-scale position range
min_position = min(predicted_positions)
max_position = max(predicted_positions)
predicted_positions = (predicted_positions - min_position) / (max_position - min_position) * 150 + 1
predicted_positions_rounded = np.round(predicted_positions).astype(int)


# Step 8: Add predicted positions as a new column to pokestats_sorted DataFrame
pokestats_sorted[f'POSITION_{Stats}'] = predicted_positions_rounded
pokestats_sorted[f'POSITION_FLOAT_{Stats}'] = predicted_positions

############### same for tiers ################

model_tiers = RandomForestRegressor()  # You can try other models as well

# Step 5: Model Training
X_train_tiers = pokepos_sorted[[Stats]]  # Using the selected stat as the feature
y_train_tiers = pokepos_sorted['TIERS']  # Target variable
model_tiers.fit(X_train_tiers, y_train_tiers)

# Step 7: Prediction

X_test_tiers = pokestats_sorted[[Stats]]  # Using the selected stat as the feature
predicted_positions_tiers = model_tiers.predict(X_test_tiers)
predicted_positions_tiers_rounded = np.round(predicted_positions_tiers).astype(int)

# Step 8: Add predicted positions as a new column to pokestats_sorted DataFrame
pokestats_sorted[f'TIERS_{Stats}'] = predicted_positions_tiers_rounded
pokestats_sorted[f'TIERS_FLOAT_{Stats}'] = predicted_positions_tiers

############### same for all stats at once ################

model_151 = RandomForestRegressor()  # You can try other models as well

# Step 5: Model Training
X_train_151 = pokepos_sorted[['HP', 'ATT', 'DEF', 'SPD', 'SPE']]  # Features
y_train_151 = pokepos_sorted['POSITION']  # Target variable
model_151.fit(X_train_151, y_train_151)

# Step 7: Prediction for all 151 Pokémon
X_all_pokemon = pokestats_sorted[['HP', 'ATT', 'DEF', 'SPD', 'SPE']]  # Features for all 151 Pokémon
predicted_positions_all_151 = model_151.predict(X_all_pokemon)


# Transform predicted positions to 151-scale position range
min_position_151 = min(predicted_positions_all_151)
max_position_151 = max(predicted_positions_all_151)
predicted_positions_all_151 = (predicted_positions_all_151 - min_position_151) / (max_position_151 - min_position_151) * 150 + 1
predicted_positions_all_151_rounded = np.round(predicted_positions_all_151).astype(int)


# Assign scaled positions to all 151 Pokémon
pokestats_sorted['POSITION'] = predicted_positions_all_151_rounded
pokestats_sorted['POSITION_FLOAT'] = predicted_positions_all_151

############### same for tiers for all stats ################

model_tiers_151 = RandomForestRegressor()  # You can try other models as well

# Step 5: Model Training
X_train_tiers_151 = pokepos_sorted[['HP', 'ATT', 'DEF', 'SPD', 'SPE']]  # Using the selected stat as the feature
y_train_tiers_151 = pokepos_sorted['TIERS']  # Target variable
model_tiers_151.fit(X_train_tiers_151, y_train_tiers_151)

# Step 7: Prediction

X_all_pokemon_tiers = pokestats_sorted[['HP', 'ATT', 'DEF', 'SPD', 'SPE']]  # Features for all 151 Pokémon
predicted_tiers_all_151 = model_tiers_151.predict(X_all_pokemon_tiers)
predicted_tiers_all_151_rounded = np.round(predicted_tiers_all_151).astype(int)

# Step 8: Add predicted positions as a new column to pokestats_sorted DataFrame
pokestats_sorted['TIERS'] = predicted_tiers_all_151_rounded
pokestats_sorted['TIERS_FLOAT'] = predicted_tiers_all_151

pokestats_sorted['TRUE_TIERS'] = pokestats_sorted['TIERS'].map({v: k for k, v in Tiers_map.items()})

################# ploting stat by stat ####################

fig_stats = go.Figure()

# Loop through pokestats_sorted to add scatter points and images
for index, row in pokestats_sorted.iterrows():
    number = row['NUMBER'] - 1
    sprite = pokesprites['SPRITE_NAME'].iloc[number]
    sprite_src = "../static/" + sprite
    with open(sprite_src, "rb") as f:
        sprite_f = base64.b64encode(f.read()).decode("utf-8")
    value = row[Stats]
    colordt = Tiers_palette.get(row[f'TIERS_{Stats}'])

    # Add scatter plot point
    scat_stats = go.Scatter(
        x=[row[f'POSITION_{Stats}']],
        y=[value],
        mode='markers',
        marker=dict(
            color=colordt,
            symbol='circle',
            size=10
        ),
        name=row['TRUE_TIERS'],
        text=row['POKEMON'] +
            '<br>' + "Tier : " + str(row[f'TIERS_{Stats}']) +
            '<br>' + "Precise tier : " + str(round(row[f'TIERS_FLOAT_{Stats}'],2)) +
            '<br>' + "Stats : " + str(value) +
            '<br>' + "Position : " + str(row[f'POSITION_{Stats}']) +
            '<br>' + "Precise position : " + str(round(row[f'POSITION_FLOAT_{Stats}'],2)),
        hoverinfo='text',
        showlegend=False,
        hoverlabel=dict(
        bgcolor=colordt,
        font=dict(color='#2d2928', family = 'Times New Roman',size=16),
        bordercolor='#f2f2f2',
        ),
    )
    fig_stats.add_trace(scat_stats)

    if pokebutton_pos:
        # Add image overlay
        fig_stats.add_layout_image(
            source='data:image/png;base64,' + sprite_f,
            x=row[f'POSITION_{Stats}'],
            y=value,
            xanchor="center",
            yanchor="middle",
            sizex=15,
            sizey=15,
            xref="x",
            yref="y"
        )

# Update layout
fig_stats.update_layout(
    xaxis=dict(title='Position',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title=Stats,
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': f"Scatter Plot of the prediction for Pokemon position in function of {Stats}",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100)
)

# Display the plot using Streamlit
st.plotly_chart(fig_stats)


############### ploting all #################

fig_all = go.Figure()

# Loop through pokestats_sorted to add scatter points and images
for index, row in pokestats_sorted.iterrows():
    number = row['NUMBER'] - 1
    sprite = pokesprites['SPRITE_NAME'].iloc[number]
    sprite_src = "../static/" + sprite
    with open(sprite_src, "rb") as f:
        sprite_f = base64.b64encode(f.read()).decode("utf-8")
    value_all = row['TOT']
    color = Tiers_palette.get(row['TIERS'])

    # Add scatter plot point
    scat_all = go.Scatter(
        x=[row['POSITION']],
        y=[value_all],
        mode='markers',
        marker=dict(
            color=color,
            symbol='circle',
            size=10
        ),
        name=row['TRUE_TIERS'],
        text=row['POKEMON'] +
            '<br>' + "Tier : " + str(row['TIERS']) +
            '<br>' + "Precise tier : " + str(round(row['TIERS_FLOAT'],2)) +
            '<br>' + "Stats : " + str(row['TOT']) +
            '<br>' + "Position : " + str(row['POSITION']) +
            '<br>' + "Precise position : " + str(round(row['POSITION_FLOAT'],2)),
        hoverinfo='text',
        showlegend=False,
        hoverlabel=dict(
        bgcolor=color,
        font=dict(color='#2d2928', family = 'Times New Roman',size=16),
        bordercolor='#f2f2f2',
        ),
    )
    fig_all.add_trace(scat_all)

    if pokebutton_pos:
        # Add image overlay
        fig_all.add_layout_image(
            source='data:image/png;base64,' + sprite_f,
            x=row['POSITION'],
            y=value_all,
            xanchor="center",
            yanchor="middle",
            sizex=15,
            sizey=15,
            xref="x",
            yref="y"
        )

# Update layout
fig_all.update_layout(
    xaxis=dict(title='Position',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    yaxis=dict(title='All stats',
        tickfont=dict(size=20),
        titlefont=dict(size=25)),
    width=1280,  # Adjust the width of the plot
    height=720,  # Adjust the height of the plot
    title={
        'text': "Scatter Plot of the prediction for Pokemon position in function of all Stats",
        'x': 0.5,  # Set title's x position to center
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 30}
    },
    margin=dict(t=100)
)

# Display the plot using Streamlit
st.plotly_chart(fig_all)