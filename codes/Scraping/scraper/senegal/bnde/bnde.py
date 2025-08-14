import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

"""from bs4 import BeautifulSoup

# Read the HTML content
json_file_path = "/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bnde/bnde.js" 

# Load the JSON file
with open(json_file_path, 'r') as file:
    html_content = file.read()


features = json.loads(html_content)

data_lba=[]

# Process and print the extracted data
for feature in features:
    lat = feature['lat']
    lon = feature['lon']
    data_lba.append({
        "Latitude": lat,
        "Longitude": lon
    })

data_senegal={"senegal":data_lba}

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bnde/bnde.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_senegal, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")

"""
with open('senegal/bnde/bnde.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []
for branch in data["senegal"]:
    senegal_data.append({
        "bank": "bnde",
        "country": "senegal",
        "address": "agence bnde",  # Address not available in the data
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open('result/json_data_all/bnde_senegal.json', 'w', encoding='utf-8') as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame

df = pd.DataFrame(data['senegal'])

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bnde/bnde.shp')
 
"""