"""
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


# Sample HTML content (the provided HTML snippet)
html_content = '''<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-2101 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-2101" data-markertitle="Agence centrale siège (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.360758" data-markerlon="-1.516811" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-siege.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-2563 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-2563" data-markertitle="10 Yaar (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.374663" data-markerlon="-1.554569" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-2558 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-2558" data-markertitle="Grand Marché (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.36733" data-markerlon="-1.52452" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3196 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3196" data-markertitle="Ouagarinter (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.335075" data-markerlon="-1.509971" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-4358 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-4358" data-markertitle="Saaba" data-markerfor="toutes-representations" data-markerlat="12.238333" data-markerlon="-1.561593" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3396 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3396" data-markertitle="Sankariaré (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.376372" data-markerlon="-1.53125" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3199 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3199" data-markertitle="Wemtenga (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.375201" data-markerlon="-1.4858" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3249 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3249" data-markertitle="Banfora" data-markerfor="toutes-representations" data-markerlat="10.640101" data-markerlon="-4.758804" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-2106 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-2106" data-markertitle="Bobo Dioulasso" data-markerfor="toutes-representations" data-markerlat="11.174005" data-markerlon="-4.303048" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-2573 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-2573" data-markertitle="Manga" data-markerfor="toutes-representations" data-markerlat="11.66503" data-markerlon="-1.063402" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3232 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3232" data-markertitle="Tenkodogo" data-markerfor="toutes-representations" data-markerlat="11.797164" data-markerlon="-0.37315" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-agence.png" data-markericonhover="" data-streetview="no" data-fromview=""></div>
<div style="display:none" class="wpv-addon-maps-marker js-wpv-addon-maps-marker js-wpv-addon-maps-marker-representation-3764 js-wpv-addon-maps-markerfor-toutes-representations" data-marker="representation-3764" data-markertitle="Eco Oil Garghin (Ouagadougou)" data-markerfor="toutes-representations" data-markerlat="12.353536" data-markerlon="-1.513882" data-markericon="//wendkunibank.bf/wp-content/uploads/pin-distributeur.png" data-markericonhover="" data-streetview="no" data-fromview="">
</div>'''

# Step 1: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 2: Extract relevant data
agencies = []

for marker in soup.find_all('div', class_='wpv-addon-maps-marker'):
    # Extracting agency name
    name = marker.get('data-markertitle', '').strip()
    
    # Extracting latitude and longitude
    latitude = marker.get('data-markerlat', '')
    longitude = marker.get('data-markerlon', '')
    
    # Storing extracted data in a dictionary
    agency_info = {
        'name': name,
        'latitude': latitude,
        'longitude': longitude
    }
    agencies.append(agency_info)

# Step 3: Print extracted data
for agency in agencies:
    print(f"Agency Name: {agency['name']}")
    print(f"Latitude: {agency['latitude']}")
    print(f"Longitude: {agency['longitude']}")
    print('-' * 40)

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/wendkuni/wendkuni.json', 'w', encoding='utf-8') as f:
    json.dump(agencies, f, indent=4)
"""
import json
with open('burkina/wendkuni/wendkuni.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

burkina_data = []
for agency in data:
    burkina_data.append({
        "bank": "wendkuni",
        "country": "burkina",
        "address": agency["name"][:80],
        "Latitude": agency["latitude"],
        "Longitude": agency["longitude"],
        "geocoded": 0
    })

with open('result/json_data_all/wendkuni.json', 'w', encoding='utf-8') as f:
    json.dump(burkina_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd

df = pd.DataFrame(data)

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/wendkuni/wendkuni.shp')"""