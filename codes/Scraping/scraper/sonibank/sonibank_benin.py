"""
import requests
from bs4 import BeautifulSoup
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



address="Cotonou, Ganhi immeuble KODEIH, Rue du Gouverneur Bayol"
latitude, longitude = get_coordinates(address, api_key)

country_data={}
country_data['benin'] = [{
    'agence': "Sonibank, succursale du Bénin",
    'Latitude': latitude,
    'Longitude': longitude
}]


# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/sonibank/sonibank_benin_geocoded.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
"""
import json
import pandas as pd
with open('sonibank/sonibank_benin_geocoded.json', 'r') as f:
    data_all = json.load(f)

sonibank_data = []
for country, branches in data_all.items():
    for branch in branches:
        sonibank_data.append({
            "bank": "sonibank",
            "country": country,
            "address": branch["agence"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })
with open("result/json_data_all/sonibank.json", "w", encoding="utf-8") as f:
    json.dump(sonibank_data, f, ensure_ascii=False, indent=4)
"""
df = pd.DataFrame(data_all['benin'])

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/sonibank/sonibank.shp')

"""