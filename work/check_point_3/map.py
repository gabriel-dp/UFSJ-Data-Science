import folium

MAP_JSON_PATH = '../data/br_states.json'

def generate_map (name, data, columns, fill_color, legend_name): 
    # Initial map setup
    map = folium.Map(
        location=[-15.795771, -50.524646],
        zoom_start=4,
        min_zoom=4,
        max_zoom=7,
    )

    # Map data
    folium.Choropleth(
        geo_data=MAP_JSON_PATH,
        name=name,
        data=data,
        columns=columns,
        key_on='feature.id',
        fill_color=fill_color,
        fill_opacity=0.5,
        line_opacity=1,
        legend_name=legend_name
    ).add_to(map)

    folium.LayerControl().add_to(map)
    
    return map