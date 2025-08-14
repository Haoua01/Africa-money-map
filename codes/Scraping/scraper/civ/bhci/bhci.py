
import pandas as pd
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


with open('civ/bhci/bhci.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

civ_data = []
for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "bhci",
        "country": "civ",
        "address": branch["title"][:80],
        "Latitude": float(branch["lat"]),
        "Longitude": float(branch["lng"]),
        "geocoded": 0
    })
with open("result/json_data_all/bhci.json", "w", encoding="utf-8") as f:
    json.dump(civ_data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data['cotedivoire'])
df.rename(columns={'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bhci/bhci.shp')"""