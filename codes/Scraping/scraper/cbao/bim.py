"""
import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse, parse_qs
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





# Le pays de l'agence, à ajuster selon le pays spécifique
country = ["Mali"]

country_code={
    "Mali": "https://www.goafricaonline.com/ml/157459-bim-banque-internationale-pour-le-mali-bamako-mali",
}

country_data={}
for country, url in country_code.items():
    # URL de la page à scraper (remplacez par l'URL réelle)
    url = url
    # Faire une requête GET pour obtenir la page HTML
    response = requests.get(url)

    # Parser la page avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les agences dans la liste (balise <li>)
    agencies = soup.find_all('li', class_='mb-6')

    # Initialiser une liste pour stocker les données des agences
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
        name_address = name_address.replace("  ", "'")
        name_address_full = f"BIM - {name_address}"
        lat,lon=get_coordinates(name_address,api_key)

        # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
        agency_info = {
            'agence': name_address[:88],
            'Latitude': lat,
            'Longitude': lon
        }

        # Ajouter l'agence à la liste
        agency_data.append(agency_info)
    country_data[country]=agency_data

# Sauvegarder les données dans un fichier JSON
with open('cbao/bim_goafrica.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)


with open('cbao/bim_goafrica_corrected.json', "r") as f:
    data = json.load(f)

import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Mali'])

#fill lat and lon when null with the geocoding api
for index, row in df.iterrows():
    if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
        lat,lon=get_coordinates(row['agence'],api_key)
        print(row['agence']), print(lat), print(lon)

        df.at[index, 'Latitude'] = lat
        df.at[index, 'Longitude'] = lon

#keepthe 50 first characters of "agence"
df['agence'] = df['agence'].str[:50]

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('cbao/bim.shp')
"""
import json
import pandas as pd

with open('cbao/bim_goafrica_corrected.json', "r") as f:
    data = json.load(f)

mali_data = []
for country, country_info in data.items():
    for branch in country_info:
        mali_data.append({
            "bank": "bim",
            "country": country,
            "address": branch["agence"][7:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })

df = pd.DataFrame(mali_data)
with open('result/json_data_all/bim.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

