"""
import requests
import json
import pandas as pd
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

url = "https://bci-banque.com/wp-admin/admin-ajax.php"

querystring = {"action":"store_search","lat":"12.63917","lng":"-8.00255","max_results":"25","search_radius":"50","filter":"44","autoload":"1"}

payload = ""
headers = {
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://bci-banque.com/mali/agences/",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

country_data={}
country_data["mali"]=response.json()

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bci/bci.json", "w") as f:
    f.write(json.dumps(country_data, indent=4))
"""
import json
with open("mali/bci/bci.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mali_data = []
for branch in data["mali"]:
    mali_data.append({
        "bank": "bci",
        "country": "mali",
        "address": (branch["store"]+ ', ' + branch['city'])[:80],
        "Latitude": float(branch["lat"]),
        "Longitude": float(branch["lng"]),
        "geocoded": 0
    })

with open("result/json_data_all/bci.json", "w", encoding="utf-8") as f:
    json.dump(mali_data, f, indent=4)
"""
df = pd.DataFrame(data["mali"])

#rename columns
df.rename(columns={'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

#gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bci/bci.shp")
"""