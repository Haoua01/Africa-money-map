
"""import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

country_data={}


from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis la variable d'environnement
api_key = os.getenv("GOOGLE_GEOCODING_API_KEY")


# Fonction pour obtenir les coordonnées via l'API Geocoding
def get_coordinates(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        print(f"Erreur de géocodage pour l'adresse : {address}")
        return None, None



address_benin="Cotonou, Boulevard St Michel, Immeuble Espace"
address_niger="Terminus, rue Heinrich Lubke n°7 - Niamey, Niger"
latitude_benin, longitude_benin = get_coordinates(address_benin, api_key)

country_data={}
country_data['benin'] = [{
    'agence': "CBAO, succursale du Bénin",
    'Latitude': latitude_benin,
    'Longitude': longitude_benin
}]

latitude_niger, longitude_niger = get_coordinates(address_niger, api_key)
country_data['niger'] = [{
    'agence': "CBAO, succursale du Niger",
    'Latitude': latitude_niger,
    'Longitude': longitude_niger
}]

adresses_burkina=["479, Avenue du Président Sangoulé Lamizana – Ouagadougou", 
                  "Boulevard Charles De gaulle - Ouagadougou - Ouagadougou - Burkina Faso",
                  "Boulevard de l’insurrection populaire - Ouagadougou - Burkina Faso Ex Blvd France Afrique",
                  "Avenue de la Nation - Ouagadougou - Burkina Faso",
                  "Avenue Babanguida - Ouagadougou"
                  "Avenue Gouverneur Delafosse, Bobo-Dioulasso"]

branch_data=[]
for i in range(len(adresses_burkina)):
    latitude, longitude = get_coordinates(adresses_burkina[i], api_key)
    branch_data.append({
        'agence': f"agence {i}, CBAO, succursale du Burkina Faso",
        'Latitude': latitude,
        'Longitude': longitude
    })
country_data['burkina'] = branch_data

url = "https://cbaobank.com/fr/vactory/locator/list/all"

payload = ""
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": "_ga=GA1.1.1176445509.1737989405; OptanonAlertBoxClosed=2025-01-27T15:10:08.311Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jan+27+2025+16%3A10%3A08+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f244af3b-7584-4178-8dfb-ae87ed681b90&interactionCount=2&landingPath=NotLandingPage&groups=; _ga_C8XH6EVXT1=GS1.1.1737989405.1.1.1737990620.0.0.0",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://cbaobank.com/fr/trouver-une-agence",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.request("GET", url, data=payload, headers=headers)

branch_data=[]
#keep only the useful data inside "results"
for branch in response.json()["results"]:
    agency_name = branch["name"]
    latitude = float(branch["field_locator_info"]["lat"])
    longitude = float(branch["field_locator_info"]["lon"])
    address = branch["field_locator_adress_address_line1"]
    branch_data.append({
        "agence": agency_name,
        "address": address,
        "Latitude": latitude,
        "Longitude": longitude
    })
country_data["senegal"] = branch_data

import json
with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/cbao_geocoded.json", "w", encoding="utf-8") as f:
    json.dump(country_data, f, indent=4)

print("Données sauvegardées")
"""
import pandas as pd
import json

with open("cbao/cbao_geocoded.json", "r", encoding="utf-8") as f:
    data_all = json.load(f)

data = []
for country, country_info in data_all.items():
    if country == "senegal":
        for branch in country_info:
            data.append({
                "bank": "cbao",
                "country": country,
                "address": branch["address"][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                "geocoded": 0
            })
    else:
        for branch in country_info:
            data.append({
                "bank": "cbao",
                "country": country,
                "address": branch["agence"][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                "geocoded": 1
            })

df = pd.DataFrame(data)
print(df.head())

with open("result/json_data_all/cbao.json", "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=4)

"""

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/cbao.shp')


"""