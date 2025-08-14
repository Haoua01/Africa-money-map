import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

with open('niger/bcn&brm/bcn.json') as f:
    data = json.load(f)

import pandas as pd
df1 = pd.DataFrame(data["bcn"])
df2 = pd.DataFrame(data["brm"])

bcn_data = []
for branch in df1.to_dict(orient="records"):
    bcn_data.append({
        "bank": "bcn",
        "country": "niger",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
brm_data = []
for branch in df2.to_dict(orient="records"):
    brm_data.append({
        "bank": "brm",
        "country": "niger",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open('result/json_data_all/bcn.json', 'w', encoding='utf-8') as f:
    json.dump(bcn_data, f, ensure_ascii=False, indent=4)

with open('result/json_data_all/brm.json', 'w', encoding='utf-8') as f:
    json.dump(brm_data, f, ensure_ascii=False, indent=4)


"""
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df1["Longitude"], df1["Latitude"])]
gdf1 = GeoDataFrame(df1, geometry=geometry)
gdf2= GeoDataFrame(df2, geometry=geometry)

gdf1.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/bcn&brm/bcn.shp')
gdf2.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/bcn&brm/brm.shp')
"""

