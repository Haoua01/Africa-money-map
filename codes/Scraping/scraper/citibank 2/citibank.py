
import pandas as pd
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent



with open('citibank 2/citibank.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

all_data = []
for country, branches in data.items():
    for branch in branches:
        all_data.append({
            "bank": "citibank",
            "country": country,
            "address": branch["Branch"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })

with open('result/json_data_all/citibank.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data['senegal'])

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/citibank/citibank_senegal.shp')

df2 = pd.DataFrame(data['cotedivoire'])
geometry2 = [Point(xy) for xy in zip(df2["Longitude"], df2["Latitude"])]
gdf2 = gpd.GeoDataFrame(df2, geometry=geometry2)

gdf2.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/citibank/citibank_cotedivoire.shp')
"""