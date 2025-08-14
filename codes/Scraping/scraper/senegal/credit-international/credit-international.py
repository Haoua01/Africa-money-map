
import pandas as pd
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

with open('senegal/credit-international/ci-senegal.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []
for branch in data["senegal"]:
    senegal_data.append({
        "bank": "credit_international",
        "country": "senegal",
        "address": branch["Branch"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
with open('result/json_data_all/credit_international.json', 'w', encoding='utf-8') as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data['senegal'])

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/credit-international/credit-international-senegal.shp')"""