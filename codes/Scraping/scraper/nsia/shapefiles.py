import json
import pandas as pd
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

"""

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_benin.json', 'r', encoding='utf-8') as f:
    data_benin = json.load(f)

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_civ.json', 'r', encoding='utf-8') as f:
    data_civ = json.load(f)

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_senegal.json', 'r', encoding='utf-8') as f:
    data_senegal = json.load(f)

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/togo_goafrica.json', 'r', encoding='utf-8') as f:
    data_togo = json.load(f)

#create combined json
data = {
    'benin': data_benin["benin"],
    'cotedivoire': data_civ["cotedivoire"],
    'senegal': data_senegal["senegal"],
    'togo': data_togo["Togo"]
}

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_coordinates_all.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
"""

with open('nsia/nsia_coordinates_all.json', 'r') as f:
    data_all = json.load(f)

country_data = []
for country, country_info in data_all.items():
    if country == "togo":
        for branch in country_info:
            country_data.append({
                'bank': "nsia",
                'country': country,
                'address': branch['agence'][7:80],
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude'],
                'geocoded': 1

            })
    elif country == "cotedivoire":
        for branch in country_info:
            country_data.append({
                'bank': "nsia",
                'country': "civ",
                'address': branch['address'][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                'geocoded': 0
            })
    elif country == "benin":
        for branch in country_info:
            country_data.append({
                'bank': "nsia",
                'country': "benin",
                'address': branch['address'][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                'geocoded': 0
            })
    else:
        for branch in country_info:
            country_data.append({
                'bank': "nsia",
                'country': country,
                'address': branch['address'][:80],
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude'],
                'geocoded': 1
            })

with open('result/json_data_all/nsia.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(country_data)
print(df.head())

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/nsia/nsia_geocoded.shp')



"""