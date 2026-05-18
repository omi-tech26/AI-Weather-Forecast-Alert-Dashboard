import folium
import json

# LOAD CITY COORDINATES

with open("data/cities.json","r") as file:
    city_data = json.load(file)

# GENERATE DYNAMIC MAP

def generate_map(city):

    # GET LATITUDE & LONGITUDE

    lat = city_data[city]["lat"]
    lon = city_data[city]["lon"]

    # CREATE MAP

    map_obj = folium.Map(
        location=[lat, lon],
        zoom_start=8
    )

    # ADD MARKER

    folium.Marker(
        [lat, lon],

        popup=f"{city} Weather Location",

        tooltip=f"{city}",

        icon=folium.Icon(
            color="red",
            icon="cloud"
        )

    ).add_to(map_obj)
    
    folium.Circle(
    radius=5000,
    location=[lat, lon],
    color="blue",
    fill=True
).add_to(map_obj)

    # SAVE MAP

    map_obj.save("outputs/weather_map.html")

    return map_obj