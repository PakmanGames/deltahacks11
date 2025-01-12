import streamlit as st
import folium
import random
import pandas as pd
import requests
from folium import GeoJson

# Function to generate random locations and dementia statistics
def generate_dementia_data():
    # List of random locations (e.g., countries or cities)
    locations = [
        {"name": "United States", "lat": 37.0902, "lon": -95.7129, "dementia_rate": 6.2},
        {"name": "Germany", "lat": 51.1657, "lon": 10.4515, "dementia_rate": 5.5},
        {"name": "Japan", "lat": 36.2048, "lon": 138.2529, "dementia_rate": 7.8},
        {"name": "Brazil", "lat": -14.2350, "lon": -51.9253, "dementia_rate": 4.1},
        {"name": "India", "lat": 20.5937, "lon": 78.9629, "dementia_rate": 3.5},
        {"name": "United Kingdom", "lat": 51.5074, "lon": -0.1278, "dementia_rate": 6.0},
    ]
    
    return pd.DataFrame(locations)

# Generate random dementia data
df = generate_dementia_data()

# Streamlit page configuration
st.set_page_config(page_title="Dementia and Alzheimer's Awareness", layout="wide")

# Homepage Title
st.markdown("""
        <h1 style="text-align: center;">Memory Lane</h1>
        <h3 style="text-align: center;">50 Million People Need our Help.</h3>
""", unsafe_allow_html=True)

# Load a GeoJSON of world countries (we will fetch it from an online source)
url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
response = requests.get(url)
countries_geojson = response.json()

# Function to generate random colors
def random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'  # Random hex color

# Create a folium map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add colored countries to the map
for feature in countries_geojson['features']:
    country_name = feature['properties']['name']
    
    # Get the dementia rate for the country from the dataframe
    dementia_rate = df[df['name'] == country_name]['dementia_rate'].values
    color = random_color() if len(dementia_rate) == 0 else random_color()  # If no rate data is found, use random color
    
    # Add the GeoJson with the random color
    folium.GeoJson(
        feature,
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }
    ).add_to(m)


# Add map to Streamlit
st.components.v1.html(m._repr_html_(), height=500)


st.markdown("""
        <h3 style="text-align: center;">Changing the world, one memory at a time.</h3>
""", unsafe_allow_html=True)

# Footer Section
st.markdown("""
    <hr>
    <footer>
        <p style="text-align: center;">© 2025 MemoryLane. All Rights Reserved.</p>
    </footer>
""", unsafe_allow_html=True)
