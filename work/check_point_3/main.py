import streamlit as st
from streamlit_folium import st_folium

from data_infractions import get_infractions_data
from data_vehicles import get_vehicles_data
from data_population import get_population_data
from map import generate_map


st.title("Análise de trânsito no Brasil")
st.subheader("Tecnologias para Data Science")


### Retrieve data
@st.cache_data
def get_all_data():
    vehicles_data = get_vehicles_data()
    population_data = get_population_data()
    infractions_data = get_infractions_data()

    vehicles_population_data = vehicles_data.merge(population_data, on=['state', 'year'], suffixes=('_df1', '_df2'))
    vehicles_population_data['quantity'] = vehicles_population_data['quantity_df1'] / vehicles_population_data['quantity_df2']
    
    infractions_vehicles_data = infractions_data.merge(vehicles_data, on=['state', 'year'], suffixes=('_df1', '_df2'))
    infractions_vehicles_data['quantity'] = infractions_vehicles_data['quantity_df1'] / infractions_vehicles_data['quantity_df2']

    return {
        'vehicles': vehicles_data,
        'population': population_data,
        'infractions': infractions_data,
        'vehicles_population': vehicles_population_data,
        'infractions_vehicles': infractions_vehicles_data,
    }

data = get_all_data()
###


### Select map
st.write("Selecione o mapa:")

MAP_OPTIONS = {
    "population": "População",
    "vehicles": "Frota",
    "infractions": "Infrações",
    "vehicles_population": "Frota / População",
    "infractions_vehicles": "Infrações / Frota",
}

def select_button(button_name):
    st.session_state.selected = button_name

if "selected" not in st.session_state:
    st.session_state.selected = 'population'

cols = st.columns(len(MAP_OPTIONS))
for col, (key, label) in zip(cols, MAP_OPTIONS.items()):
    with col:
        st.button(label, on_click=select_button, args=(key,), disabled=st.session_state.selected == key)
###


### Select year
st.write("Selecione o ano:")
all_years = data[st.session_state.selected]['year'].unique()
min_year = int(all_years.min())
max_year = int(all_years.max())

if "year" not in st.session_state or st.session_state.year not in all_years:
    st.session_state.year = max_year

selected_year = st.slider(
    "year",
    min_value=min_year,
    max_value=max_year,
    value=st.session_state.year,
    step=1,
    label_visibility="hidden"
)
###


# Filter data for the year
data_filtered = data[st.session_state.selected]
data_filtered = data_filtered[data_filtered['year'] == selected_year]


# Render the map
map_obj = generate_map("Mapa Brasil", data_filtered, ['state', 'quantity'], 'YlOrRd', MAP_OPTIONS[st.session_state.selected])
st_data = st_folium(map_obj, width='100%', height=600, returned_objects=[])
