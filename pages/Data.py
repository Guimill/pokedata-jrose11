import pandas as pd
import streamlit as st

type_pal_old={"Dragon":"#4f60e2","Electrik":"#fac100","Fighting":"#ff8100","Fire":"#e72324","Ghost":"#713f71","Ground":"#92501b","Ice":"#3dd9ff","Insect":"#92a312","Normal":"#a0a3a0","Plant":"#3da324","Poison":"#923fcc","Psychic":"#ef3f7a","Rock":"#b1ab82","Water":"#2481ef","Fly":"#82baef"}
type_pal_new={"Dragon":"#036dc4","Electrik":"#f4d339","Fighting":"#cf3f6b","Fire":"#ff9e54","Ghost":"#5169ae","Ground":"#da7943","Ice":"#74cfc1","Insect":"#92c22b","Normal":"#929ba3","Plant":"#63bb5a","Poison":"#ac6bc9","Psychic":"#fa727a","Rock":"#c6b88d","Water":"#4f91d7","Fly":"#90abdf"}
dt_type_pal_new={"Dragon":"#036dc4","Dragon/Fly":["#036dc4","#90abdf"],"Electrik":"#f4d339","Electrik/Fly":["#f4d339","#90abdf"],"Fighting":"#cf3f6b","Fire":"#ff9e54","Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":"#da7943","Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":"#92c22b","Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":"#929ba3","Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":"#ac6bc9","Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":"#fa727a","Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":"#4f91d7","Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}
dt_type_pal_new_double={"Dragon":["#036dc4","#036dc4"],"Dragon/Fly":["#036dc4","#90abdf"],"Electrik":["#f4d339","#f4d339"],"Electrik/Fly":["#f4d339","#90abdf"],"Fighting":["#cf3f6b","#cf3f6b"],"Fire":["#ff9e54","#ff9e54"],"Fire/Fly":["#ff9e54","#90abdf"],"Ghost/Poison":["#5169ae","#ac6bc9"],"Ground":["#da7943","#da7943"],"Ground/Poison":["#da7943","#ac6bc9"],"Ground/Rock":["#da7943","#c6b88d"],"Ice/Fly":["#74cfc1","#90abdf"],"Ice/Psychic":["#74cfc1","#fa727a"],"Insect":["#92c22b","#92c22b"],"Insect/Fly":["#92c22b","#90abdf"],"Insect/Plant":["#92c22b","#63bb5a"],"Insect/Poison":["#92c22b","#ac6bc9"],"Normal":["#929ba3","#929ba3"],"Normal/Fly":["#929ba3","#90abdf"],"Plant/Poison":["#63bb5a","#ac6bc9"],"Plant/Psychic":["#63bb5a","#fa727a"],"Poison":["#ac6bc9","#ac6bc9"],"Poison/Fly":["#ac6bc9","#90abdf"],"Psychic":["#fa727a","#fa727a"],"Rock/Fly":["#c6b88d","#90abdf"],"Rock/Ground":["#c6b88d","#da7943"],"Water":["#4f91d7","#4f91d7"],"Water/Fly":["#4f91d7","#90abdf"],"Water/Ice":["#4f91d7","#74cfc1"],"Water/Poison":["#4f91d7","#ac6bc9"],"Water/Psychic":["#4f91d7","#fa727a"]}

OLD_TYPE_PALETTE = pd.DataFrame.from_dict(type_pal_old, orient = 'index', columns = ['coulours'])
NEW_TYPE_PALETTE =  pd.DataFrame.from_dict(type_pal_new,orient = 'index', columns = ['coulours'])
NEW_DTYPE_PALETTE =  pd.DataFrame.from_dict(dt_type_pal_new,orient = 'index', columns = ['coulours'])
NEW_DTYPE_PALETTE_DOUBLE =  pd.DataFrame.from_dict(dt_type_pal_new_double,orient = 'index', columns = ['1 type col','2 type col'])

POKEDATA = pd.read_csv('/workspaces/pokedata-jroose11/data/pokedata.csv', sep = ';')
POKEMOVES = pd.read_csv('/workspaces/pokedata-jroose11/data/Full_Moves.csv', sep = ';')
ATT_MOVES = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_ATT_MOVES.csv', sep = ';')
STATUS_MOVES = pd.read_csv('/workspaces/pokedata-jroose11/data/FULL_STATUS_MOVES.csv', sep = ';')
JROOSE11 = pd.read_csv('/workspaces/pokedata-jroose11/data/JROOSE11.csv', sep = ';')


# Define replacement values for NaN based on data types
replace_values = {'int64': 0, 'float64': 0.0, 'object': ''}

# Replace NaN with appropriate placeholders based on data types
for column in POKEDATA.columns:
    POKEDATA[column].fillna(replace_values.get(str(POKEDATA[column].dtype), ''), inplace=True)

for column in POKEMOVES.columns:
    POKEMOVES[column].fillna(replace_values.get(str(POKEMOVES[column].dtype), ''), inplace=True)

for column in ATT_MOVES.columns:
    ATT_MOVES[column].fillna(replace_values.get(str(ATT_MOVES[column].dtype), ''), inplace=True)

for column in STATUS_MOVES.columns:
    STATUS_MOVES[column].fillna(replace_values.get(str(STATUS_MOVES[column].dtype), ''), inplace=True)

for column in JROOSE11.columns:
    JROOSE11[column].fillna(replace_values.get(str(JROOSE11[column].dtype), ''), inplace=True)

data = st.radio("Choose the dataframe you'd like to display :",
                     ["JROOSE11","POKEDATA","ATT_MOVES","STATUS_MOVES","POKEMOVES","OLD_TYPE_PALETTE","NEW_TYPE_PALETTE","NEW_DTYPE_PALETTE","NEW_DTYPE_PALETTE_DOUBLE"],
                     horizontal = True)

st.dataframe(locals()[data])
