"""
from bs4 import BeautifulSoup
import requests
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

html_path = '/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/bim.html'
agency_list = []
# Read the HTML file
with open(html_path, 'r') as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Trouver toutes les agences dans la liste (balise <li>)
agencies = soup.find_all('li', class_='mb-6')

# Initialiser une liste pour stocker les données des agences
agency_data = []

# Extraire les informations de chaque agence
for agency in agencies:
    # Trouver le nom de l'agence et l'adresse dans les balises <address>
    address_tag = agency.find('address', class_='m-0 mb-2 text-gray-700')
    
    # Extraire le texte nettoyé
    name_address = address_tag.get_text(separator=' ', strip=True)
    name_address = name_address.replace("  ", "'")
    lat,lon=get_coordinates(name_address,api_key)

    # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
    agency_dict = {
        'agence': name_address[:88],
        'Latitude': lat,
        'Longitude': lon
    }
    agency_list.append(agency_dict)

# Output the list of dictionaries
print(agency_list)

country_data={}
country_data["mali"]=agency_list

# Save the data to a JSON file
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/bim2.json', 'w') as f:
    json.dump(country_data, f, indent=4)
"""
import json
# Read the JSON file
with open('cbao/bim2.json', 'r') as f:
    data = json.load(f)

mali_data = []
for country, country_info in data.items():
    for branch in country_info:
        mali_data.append({
            "bank": "bim",
            "country": country,
            "address": branch["agence"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })
import pandas as pd
df = pd.DataFrame(mali_data)
with open('result/json_data_all/bim.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

"""


# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mali'])

# Save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/bim2_geocoded.shp')
"""