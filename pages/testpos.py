import pandas as pd
import streamlit as st
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ImageURL
import statsmodels.api as sm

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

# data_option selection and data preparation...

data_option = st.selectbox("Select from these dataframes :",
                     ("FULL", "Without Mewtwo", "Without Mewtwo and the KO's", "Without the KO's"),
                     index=0, placeholder="Select the dataframe you'd like to use...")

if data_option == "FULL":
    data = pokedata.copy()  # If you want to use the full DataFrame
elif data_option == "Without Mewtwo":
    data = pokedata.iloc[1:].copy()  # Excluding the first row
elif data_option == "Without Mewtwo and the KO's":
    data = pokedata.iloc[1:-3].copy()  # Excluding the first row and the last three rows
elif data_option == "Without the KO's":
    data = pokedata.iloc[:-3].copy()  # Excluding the last three rows

Stats = st.radio("Choose the Stats you'd like to display :",
                 ["HP", "ATT", "DEF", "SPD", "SPE", "BULK", "TOT", "LEVEL", "NUMBER"],
                 horizontal=True)

pokepos_sorted = data.sort_values(by=Stats)

# Bokeh plot creation...
fig = figure(title="Scatter Plot of Pokemon Stats vs. Position", x_axis_label='Position', y_axis_label='Stats', width=1000, height=600)

# Add scatter plot layer with dots
fig.scatter(x=pokepos_sorted['POSITION'], y=pokepos_sorted[Stats], size=15, color='blue', alpha=0.5)

# Extract sprite URLs based on Pokémon name
sprite_urls = pokesprites.set_index('POKEMON')['SPRITE_URL'].to_dict()

# Add sprite glyphs for each Pokemon
for index, row in pokepos_sorted.iterrows():
    pokemon_name = row['POKEMON']  # Assuming 'POKEMON' is the column containing Pokémon names
    sprite_url = sprite_urls.get(pokemon_name)  # Retrieve sprite URL from the dictionary
    if sprite_url:
        x = row['POSITION']  # X-coordinate based on POSITION value
        y = row[Stats]  # Y-coordinate based on STATS value
        fig.image_url(url=[sprite_url], x=x, y=y, w=5, h=10, anchor="center")
    else:
        print(f"Sprite URL not found for {pokemon_name}")

# Add HoverTool with Pokémon name and DTYPES
hover = HoverTool(tooltips=[("Pokemon", "@POKEMON"), ("Type", "@DTYPES")])
fig.add_tools(hover)

# Display the Bokeh plot in Streamlit
st.bokeh_chart(fig)
