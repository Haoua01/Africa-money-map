"""
import requests
import json
import pandas as pd
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


url = "https://bms-sa.ml/wp-admin/admin-ajax.php"

querystring = {"action":"asl_load_stores","nonce":"ed12c28322","load_all":"1","layout":"1"}

payload = ""
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": "_ga=GA1.1.1912140904.1736548470; bp_ut_session=%7B-q-pageviews-q-%3A2-c--q-referrer-q-%3A-q--q--c--q-landingPage-q-%3A-q-https%3A%2F%2Fbms-sa.ml%2Fnos-agences%2F-q--c--q-started-q-%3A1739191250027%7D; _ga_J45D1DB1CJ=GS1.1.1739191203.5.1.1739191250.0.0.0",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://bms-sa.ml/nos-agences/",
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

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bms/bms.json", "w") as f:
    f.write(json.dumps(country_data, indent=4))
"""
import json
with open("mali/bms/bms.json", "r", encoding='utf-8') as f:
    data = json.load(f)

mali_data = []
for branch in data["mali"]:
    mali_data.append({
        "bank": "bms",
        "country": "mali",
        "address": (branch["street"] + ', ' + branch['city'])[:80],
        "Latitude": float(branch["lat"]),
        "Longitude": float(branch["lng"]),
        "geocoded": 0
    })

with open("result/json_data_all/bms.json", "w", encoding="utf-8") as f:
    json.dump(mali_data, f, indent=4)
"""
df = pd.DataFrame(data["mali"])

df = df[["id","lat","lng"]]
df.rename(columns={'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bms/bms-mali.shp")
"""