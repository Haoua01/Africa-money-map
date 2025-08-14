"""
import requests
from bs4 import BeautifulSoup
import json
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


url="https://www.goafricaonline.com/sn/259428-credit-banques-dakar-senegal"
response = requests.get(url)

# Parser la page avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver toutes les agences dans la liste (balise <li>)
agencies = soup.find_all('li', class_='mb-6')

# Initialiser une liste pour stocker les données des agences
country_data = {}
agency_data = []

# Extraire les informations de chaque agence
for agency in agencies:
    # Trouver le nom de l'agence et l'adresse dans les balises <address>
    address_tag = agency.find('address', class_='m-0 mb-2 text-gray-700')

        # Remplacer les <br> par " - " dans l'adresse
    for br_tag in address_tag.find_all('br'):
        br_tag.insert_before(' ')
        br_tag.insert_after(' ')
        br_tag.decompose()  # Remove <br> tag
    
    # Extraire le texte nettoyé
    name_address = address_tag.get_text(separator=' ', strip=True)

    lat, lng = get_coordinates(name_address, api_key)


    # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
    agency_info = {
        'agence': name_address[:50],
        'Latitude': lat,
        'Longitude': lng
    }

    # Ajouter l'agence à la liste
    agency_data.append(agency_info)
country_data["senegal"]=agency_data

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/cds/cds.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
"""
# Read the JSON file
import json
with open('senegal/cds/cds.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []

for branch in data['senegal']:
    senegal_data.append({
        "bank": "cds",
        "country": "senegal",
        "address": branch["agence"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open('result/json_data_all/cds.json', 'w', encoding='utf-8') as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)


"""
import pandas as pd
# Convert the JSON data to a DataFrame

df = pd.DataFrame(data['senegal'])

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/cds/cds.shp')
 
"""