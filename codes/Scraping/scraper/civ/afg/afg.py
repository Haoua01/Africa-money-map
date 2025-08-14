import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

with open("civ/afg/afg.json", "r") as f:
    data = json.load(f)

civ_data = []
for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "afg_bank",
        "country": "civ",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
with open("result/json_data_all/afg.json", "w", encoding="utf-8") as f:
    json.dump(civ_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['cotedivoire'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/afg/afg-civ.shp')"""