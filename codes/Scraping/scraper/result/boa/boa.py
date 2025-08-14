
"""
import requests
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


country_and_code = {
    "benin":"bj",
    "burkinafaso":"bf",
    "coteivoire":"ci",
    "mali":"ml",
    "niger":"ne",
    "senegal":"sn",
    "togo":"tg"

}


country_data = {}



for country, code in country_and_code.items():

    url = "https://www.boa"+country+".com/wp-admin/admin-ajax.php"

    querystring = {"action":"store_search","lat":"6.4968574","lng":"2.6288523","max_results":"25","search_radius":"50","autoload":"1"}

    payload = ""
    headers = {
        "Accept": "*/*",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "_gid=GA1.2.1894650736.1737494634; _ga_JLEBGHMF0J=GS1.2.1737494634.1.0.1737494634.0.0.0; _ga_NKJR9LD1YL=GS1.2.1737494634.1.0.1737494634.0.0.0; _ga_G5TD90NFS9=GS1.2.1737494634.1.0.1737494634.0.0.0; _gat_UA-182970593-6=1; _gat_UA-182970593-1=1; _gat_UA-149350787-8=1; _ga_QMYG6TC969=GS1.1.1737494634.1.1.1737495183.0.0.0; _ga=GA1.1.143110931.1737494634",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\""
    }

    r = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)

    country_data[country] = r.json()





#save as json
import json
import os

#create a directory to save the json file
os.makedirs("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/boa", exist_ok=True)

#save as a json file
with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/boa/boa.json", "w") as f:
    json.dump(country_data, f, indent=4)


"""

#keep "Latitude", "Longitude" and save to a csv file

import pandas as pd
import json

with open('result/boa/boa.json', "r", encoding="utf-8") as f:
    boa_data = json.load(f)

data = []

for country, country_info in boa_data.items():
    if country =="burkinafaso":
        for branch in country_info:
            data.append({
                'bank': "boa",
                'country': "burkina",
                'address': branch['address'][:80],
                'Latitude': float(branch['lat']),
                'Longitude': float(branch['lng']),
                'geocoded': 0
            })
    elif country =="coteivoire":
        for branch in country_info:
            data.append({
                'bank': "boa",
                'country': "civ",
                'address': branch['address'][:80],
                'Latitude': float(branch['lat']),
                'Longitude': float(branch['lng']),
                'geocoded': 0
            })
    else:
        for branch in country_info:
            data.append({
                'bank': "boa",
                'country': country,
                'address': branch['address'][:80],  
                "Latitude": float(branch["lat"]),
                "Longitude": float(branch["lng"]),
                'geocoded': 0
            })

with open('result/json_data_all/boa.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/boa/boa.shp")
"""