import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


with open("civ/mansa&orange&brm/mansa.json", "r") as f:
    data = json.load(f)


import pandas as pd


# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mansa_bank'])
df2 = pd.DataFrame(data['orange_bank'])
df3 = pd.DataFrame(data['brm'])

mansa_data = []
for branch in df.to_dict(orient='records'):
    mansa_data.append({
        "bank": "mansa_bank",
        "country": "civ",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
orange_data = []
for branch in df2.to_dict(orient='records'):
    orange_data.append({
        "bank": "orange_bank",
        "country": "civ",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
brm_data = []
for branch in df3.to_dict(orient='records'):
    brm_data.append({
        "bank": "brm",
        "country": "civ",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open("result/json_data_all/mansa_bank.json", "w", encoding="utf-8") as f:
    json.dump(mansa_data, f, ensure_ascii=False, indent=4)

with open("result/json_data_all/orange_bank_civ.json", "w", encoding="utf-8") as f:
    json.dump(orange_data, f, ensure_ascii=False, indent=4)

with open("result/json_data_all/brm_civ.json", "w", encoding="utf-8") as f:
    json.dump(brm_data, f, ensure_ascii=False, indent=4)

"""
from geopandas import GeoDataFrame
from shapely.geometry import Point
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)
gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/mansa&orange&brm/mansa-bank.shp')

gdf2 = GeoDataFrame(df2, geometry=geometry)
gdf2.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/mansa&orange&brm/orange-bank.shp')

gdf3 = GeoDataFrame(df3, geometry=geometry)
gdf3.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/mansa&orange&brm/brm.shp')"""