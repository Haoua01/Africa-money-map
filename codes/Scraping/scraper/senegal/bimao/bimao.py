
'''import requests
import json
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


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


url = "https://ebanking.bimao.sn/BanqueDigitale/api/services/data/branches"

payload = ""
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://ebanking.bimao.sn/PortailWeb/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "X-API-KEY": "8bb594ab3cb842e88cd95a5ff7681192",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\""
}

response = requests.request("GET", url, data=payload, headers=headers, verify=False)
agency_data = []

data_all = response.json()

for branch in data_all:
    agency_data.append({
        "agence": branch['description'],
        "Latitude": branch['latitude'],
        "Longitude": branch['longitude']
    })

data_senegal={}
data_senegal["senegal"]=agency_data

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bimao/bimao.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_senegal, json_file, ensure_ascii=False, indent=4)
'''
import json

with open('senegal/bimao/bimao.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []
for branch in data["senegal"]:
    senegal_data.append({
        "bank": "bimao",
        "country": "senegal",
        "address": branch["agence"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
with open('result/json_data_all/bimao.json', 'w', encoding='utf-8') as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['senegal'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bimao/bimao.shp')


"""