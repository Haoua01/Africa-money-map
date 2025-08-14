"""
address_af =  {
    "Agence Yirimadio": "RN6 non loin du rond-point de Wara, Bamako, Mali",
    "SIEGE": "Hamdalaye ACI 2000, rue 286 IMM M1, Bamako, Mali",
    "ZONE INDUSTRIELLE": "Zone Industrielle Route de Sotuba, immeuble Baniamey en face de Malilait SA, Bamako, Mali",
    "SUGUBA": "Grand marché, En face de l’ancienne Poste Nationale, Bamako, Mali",
    "DABANANI": "Marché Dabanani, Rue Caron, Bamako, Mali",
    "KAYES": "Quartier Liberté, Immeuble Boubacar Doucouré, Kayes, Mali",
    "AGENCE PRESTIGE": "AGENCE PRESTIGE, Avenue du Mali Immeuble Soya Bathily en face de Huawey, Bamako, Mali",
    "BADALABOUGOU": "Avenue de L’OUA, Bamako, Mali",
    "MARCHE MEDINE": "Station Shell Médine marché, près du stade Omnisport, Bamako, Mali",
    "DJELIBOUGOU": "Route de Koulikoro, station Total Djélibougou, Bamako, Mali",
    "MISSABOUGOU": "Route de Missabougou, Station Total Missagougou, Bamako, Mali",
    "SEBENICORO": "Secteur 1, RN5, Station Total Sebenicoro, Bamako, Mali"
}


import requests
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
import json
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




data_burkina = []
for key, value in address_af.items():
    lat, lng = get_coordinates(value, api_key)
    data_burkina.append({
        "name": key,
        "address": value,
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"mali": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/afg-bank/afg.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("mali/afg-bank/afg.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mali_data=[]
for branch in data["mali"]:
    mali_data.append({
        "bank": "afg_bank",
        "country": "mali",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/afg_bank.json", "w", encoding='utf-8') as f:
    json.dump(mali_data, f, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mali'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/afg-bank/afg-mali.shp')

"""
