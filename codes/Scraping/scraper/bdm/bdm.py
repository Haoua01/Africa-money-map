import requests
from bs4 import BeautifulSoup
import json
import re
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


agence= "Angle rue Boulevard du 13 janvier, Aguiarkomé, Lomé - Togo"

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

branch_data=[]
country_data={}

lat, lng = get_coordinates(agence, api_key)
branch_data.append({"agence": "BDM succursale Togo", "Latitude": lat, "Longitude": lng})
country_data["Togo"]=branch_data


with open('bdm/bdm_togo.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)


# adding Senegal data
import json
with open('bdm/bdm_togo_senegal.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

import pandas as pd


# Convert the JSON data to a DataFrame for Togo and Senegal

df = pd.DataFrame(data['Togo'])
df2 = pd.DataFrame(data['Senegal'])

data_combined = []
for country, country_info in data.items():
    if country == "Togo":
        for branch in country_info:
            data_combined.append({
                'bank': "bdm",
                'country': "togo",
                'address':  "Angle rue Boulevard du 13 janvier, Aguiarkomé, Lomé - Togo",
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude'],
                'geocoded': 1
            })
    elif country == "Senegal":
        for branch in country_info:
            data_combined.append({
                'bank': "bdm",
                'country': "senegal",
                'address': "Immeuble ClairAfrique, Place de l’Indépendance, rue Malenfant, Dakar Plateau - Sénégal",
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude'],
                'geocoded': 1
            })


df_combined = pd.DataFrame(data_combined)

with open('result/json_data_all/bdm.json', 'w', encoding='utf-8') as f:
    json.dump(df_combined.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

