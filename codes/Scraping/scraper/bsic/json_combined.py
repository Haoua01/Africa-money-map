"""
import json
import requests
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




with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/bsic/bsic_scrapped.json', 'r') as file:
    data = json.load(file)




# Fonction pour remplir les coordonnées manquantes
def fill_coordinates(country_data):
    for entry in country_data:
        if not entry.get("Latitude") or not entry.get("Longitude"):  # Vérifie si les coordonnées manquent
            #print(f"Récupération des coordonnées pour : {entry['address']}")
            latitude, longitude = get_coordinates(entry['agence'], api_key)
            
            # Si les coordonnées sont obtenues, les ajouter au JSON
            if latitude and longitude:
                entry["Latitude"] = latitude
                entry["Longitude"] = longitude


for country in data:
    print(f"Mise à jour des coordonnées pour le pays : {country}")
    fill_coordinates(data[country])


            

# Sauvegarder le fichier mis à jour
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/bsic/Geocoding/bsic_partial.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Les coordonnées manquantes ont été mises à jour.")

"""
import json
with open('bsic/Geocoding/bsic_all.json', 'r') as file:
    all_data = json.load(file)

import pandas as pd

data = []

for country, country_info in all_data.items():
    if country=="benin":
        for branch in country_info:
            data.append({
                "bank": "bsic",
                "country": "benin",
                "address": branch["address"][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                "geocoded": 1
            })
    else:
        for branch in country_info:
            data.append({
                "bank": "bsic",
                "country": country,
                "address": branch["agence"][:80],
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"],
                "geocoded": 1
            })

df = pd.DataFrame(data)
with open('result/json_data_all/bsic.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

"""

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)



gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/bsic/Geocoding/bsic_geocoded.shp")
"""