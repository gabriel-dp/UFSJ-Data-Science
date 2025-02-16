import streamlit as st
from streamlit_folium import st_folium

from data_infractions import get_infractions_data
from data_vehicles import get_vehicles_data
from data_population import get_population_data
from map import generate_map

@st.cache_data
def get_all_data():
    return {
        'vehicles': get_vehicles_data(),
        'population': get_population_data(),
        'infractions': get_infractions_data(),
    }

# Retrieve data
data = get_all_data()

# Streamlit UI
st.title("Análise dos dados de trânsito no Brasil")


st.write("Selecione o mapa:")

# Initialize session state
if "selected" not in st.session_state:
    st.session_state.selected = 'population'

# Function to handle button clicks
def select_button(button_name):
    st.session_state.selected = button_name

# Display buttons for data selection
col1, col2, col3 = st.columns(3)
with col1:
    st.button("População", 
              on_click=select_button, args=("population",), 
              disabled=st.session_state.selected == "population")
with col2:
    st.button("Frota", 
              on_click=select_button, args=("vehicles",), 
              disabled=st.session_state.selected == "vehicles")
with col3:
    st.button("Infrações", 
              on_click=select_button, args=("infractions",), 
              disabled=st.session_state.selected == "infractions")
    
all_years = data[st.session_state.selected]['year'].unique()
min_year = int(all_years.min())
max_year = int(all_years.max())

# Create a slider for year selection
selected_year = st.slider(
    "Selecione o ano:",
    min_value=min_year,
    max_value=max_year,
    value=max_year,  # Default to the most recent year
    step=1
)

# Filter data for the year 2020
data_filtered = data[st.session_state.selected]
data_filtered = data_filtered[data_filtered['year'] == selected_year]

# Render the map
map_obj = generate_map("Infractions Brazil", data_filtered, ['state', 'quantity'], 'YlOrRd', 'Infractions')
st_data = st_folium(map_obj, width='100%', height=600, returned_objects=[])
