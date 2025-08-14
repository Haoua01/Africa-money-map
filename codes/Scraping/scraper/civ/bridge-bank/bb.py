"""from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

html_path = '/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bridge-bank/bb.html'

# Step 1: Read the HTML content
with open(html_path, 'r') as file:
    html_content = file.read()

# Step 2: Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')
# Step 2: Extract relevant data
agencies = []

for card in soup.find_all('div', class_='uk-card'):
    # Extracting agency name
    name = card.find('h2', class_='agence-name').text.strip()
    
    # Extracting coordinates from the Google Maps link
    direction_link = card.find('a', href=True)['href']
    coords = direction_link.split('destination=')[-1]  # Extracting latitude,longitude
    
    latitude, longitude = coords.split(',')
    
    # Storing extracted data in a dictionary
    agency_info = {
        'name': name,
        'Latitude': latitude,
        'Longitude': longitude
    }
    agencies.append(agency_info)


country_data = {"cotedivoire": agencies}

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bridge-bank/bb.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, indent=4)
"""
import json
with open('civ/bridge-bank/bb.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data_all = []
for country, branches in data.items():
    for branch in branches:
        data_all.append({
            "bank": "bridge-bank",
            "country": "civ",
            "address": branch["name"][:80],
            "Latitude": float(branch["Latitude"]),
            "Longitude": float(branch["Longitude"]),
            "geocoded": 0
        })

with open('result/json_data_all/bridge_bank_civ.json', 'w', encoding='utf-8') as f:
    json.dump(data_all, f, ensure_ascii=False, indent=4)
"""
import pandas as pd

df = pd.DataFrame(data['cotedivoire'])


import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bridge-bank/bridge-bank-civ.shp')"""