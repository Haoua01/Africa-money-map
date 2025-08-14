"""
import requests
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent



country_and_code = {
    "benin":"bj",
    "burkinafaso":"bf",
    "cotedivoire":"ci",
    "senegal":"sn"
}


country_data = {}



for country, code in country_and_code.items():

    url = "https://www.uba"+country+".com/wp-admin/admin-ajax.php"

    querystring = {"action":"store_search","lat":"0","lng":"0","max_results":"25","search_radius":"50","autoload":"1"}

    payload = ""
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "cookie": "visid_incap_2792974=GLlB+c0oT1ak4Gac6Bz545GfgWcAAAAAQUIPAAAAAADat7dyIavEMYD5pLlnZMT0; _gcl_au=1.1.857427610.1736548244; _ga=GA1.1.2074155129.1736548244; cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-non-necessary=yes; _fbp=fb.1.1736548244592.646383857867847321; incap_ses_2224_2792974=GVlNSwipOWkJjSvlcTzdHpcdkGcAAAAAi8sUGDPSeERIOhya26i3Ug==; __stp=eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiJjYzQ5MzgwYy1jMTRiLTQyMDEtYTZjYy1mYjU0Y2UxMzBhMjkifQ==; __sts=eyJzaWQiOjE3Mzc0OTgwMDk3NzMsInR4IjoxNzM3NDk4MDA5NzczLCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy51YmFjb3RlZGl2b2lyZS5jb20lMkZhaWRlJTJGY2VudHJlLWQtYWlkZSUyRmd1aWNoZXQtYXV0b21hdGlxdWUtZXQtbG9jYWxpc2F0ZXVyLWQtYWdlbmNlcyUyRiIsInBldCI6MTczNzQ5ODAwOTc3Mywic2V0IjoxNzM3NDk4MDA5NzczfQ==; __stgeo=IjAi; __stbpnenable=MQ==; __stdf=MA==; _ga_691MDWLLPS=GS1.1.1737498008.3.1.1737498026.0.0.0; _ga_Z9P1G4QNP1=GS1.1.1737498009.3.1.1737498026.0.0.0",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.ubacotedivoire.com/aide/centre-d-aide/guichet-automatique-et-localisateur-d-agences/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    r = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    country_data[country] = r.json()





#save as json
import json
import os

#create a directory to save the json file
os.makedirs("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/uba", exist_ok=True)

#save as a json file
with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/uba/uba.json", "w") as f:
    json.dump(country_data, f, indent=4)




#remove space from Latitude and Longitude in country_data
for country, country_info in country_data.items():
    print(country)
    for atm in country_info:
        print(atm["address"])
        atm["lat"] = atm["lat"].replace(" ", "")
        atm["lng"] = atm["lng"].replace(" ", "")



import pandas as pd

data = []

for country, country_info in country_data.items():
    print(country)
    for atm in country_info:
        print(atm)
        data.append({
            "Latitude": atm["lat"],
            "Longitude": atm["lng"]
        })

df = pd.DataFrame(data)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/uba/uba.shp")
"""
import json

#open json file orabank_corrected.json and extract latitude and longitude into a shapefile
with open('result/uba/uba_corrected.json', "r", encoding="utf-8") as f:
    uba_data = json.load(f)

data = []

for country, country_info in uba_data.items():
    for branch in country_info:
        data.append({
            'bank': "uba",
            'country': country,
            'address': (branch['address']+ ', ' + branch['city'].upper())[:80],  
            "Latitude": branch["lat"],
            "Longitude": branch["lng"],
            "geocoded": 0
        })



with open('result/json_data_all/uba.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
df = pd.DataFrame(data)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)



gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/uba/uba.shp')
"""