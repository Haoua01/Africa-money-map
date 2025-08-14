import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent
"""
country_data = {}
country_data["burkina"]=[{
                    "address": "Agence 1",
                    "Latitude": "12.3583333",
                    "Longitude": "-1.5206346666666666",
                    "infobox_content": "<strong>Ouagadougou<\/strong><br>\nSecteur 5, Zone ZACA, prolongement gare TCV<br>\n1035, Avenue de la Grande Mosqu\u00e9e 01 BP 4050 Ouagadougou 01 Burkina<br>\nAdresse email : contact@badf.bf<br>\nT\u00e9l\u00e9phone : 226 25 32 99 00<br>",
                }, {
                    "address": "Agence 2",
                    "Latitude": "11.185367930898387",
                    "Longitude": "-4.307696817296282",
                    "infobox_content": "<strong>Bobo Dioulasso<\/strong><br>Adresse email : contact@badf.bf",
                }, {
                    "address": "Agence 3",
                    "Latitude": "11.4835326",
                    "Longitude": "-3.4669352",
                    "infobox_content": "<strong>Di\u00e9bougou<\/strong><br>Adresse email : contact@badf.bf",
                }, {
                    "address": "Agence 4",
                    "Latitude": "12.4621653",
                    "Longitude": "-3.4669352",
                    "infobox_content": "<strong>Banfora<\/strong><br>Adresse email : contact@badf.bf",
                }, {
                    "address": "Agence 5",
                    "Latitude": "12.3782373",
                    "Longitude": "-1.5300605",
                    "infobox_content": "<strong>Hound\u00e9<\/strong><br>Adresse email : contact@badf.bf<br>",
                }, {
                    "address": "Agence 6",
                    "infobox_content": "<strong>Sankaryar\u00e9, Ouagadougou<\/strong><br>Adresse email : contact@badf.bf<br>",
                    "Latitude": "10.637224",
                    "Longitude": "-4.756317"
                }, {
                    "address": "Agence 7",
                    "infobox_content": "<strong>D\u00e9dougou<\/strong><br>Adresse email : contact@badf.bf<br>",
                    "Latitude": "10.966028",
                    "Longitude": "-3.2487084"
                }, {
                    "address": "Agence 8",
                    "infobox_content": "13.0835278,-1.08575",
                    "Latitude": "13.0835278",
                    "Longitude": "-1.08575"
                }, {
                    "address": "Agence 9",
                    "infobox_content": "11.4902683,-0.5237717000000001",
                    "Latitude": "11.4902683",
                    "Longitude": "-0.5237717000000001"
                }]

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/badf/badf.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, indent=4)
"""
with open('burkina/badf/badf.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

burkina_data = []
for branch in data["burkina"]:
    burkina_data.append({
        "bank": "badf",
        "country": "burkina",
        "address": branch["address"][:80],
        "Latitude": float(branch["Latitude"]),
        "Longitude": float(branch["Longitude"]),
        "geocoded": 0
    })

with open('result/json_data_all/badf.json', 'w', encoding='utf-8') as f:
    json.dump(burkina_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd

df = pd.DataFrame(data['burkina'])


import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/badf/badf.shp')"""