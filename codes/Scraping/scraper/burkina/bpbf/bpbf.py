
import pandas as pd
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

with open('burkina/bpbf/bpbf.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

country_data = []
for country, branches in data.items():
    for branch in branches:
        address = branch["name"][:80]
        latitude = branch["Latitude"]
        longitude = branch["Longitude"]
        country_data.append({
            "bank": "bpbf",
            "country": country,
            "address": address,
            "Latitude": latitude,
            "Longitude": longitude,
            "geocoded": 1
        })

with open('result/json_data_all/bpbf.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, ensure_ascii=False, indent=4)


"""
df = pd.DataFrame(data['burkina'])

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/bpbf/bpbf.shp')"""