"""
import requests
from bs4 import BeautifulSoup
import json
import re
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

country_data={}

adresses_togo={
    "Agence principale":"23 Avenue Kléber Dadjo Qt, Ahanoukopé, Togo",
    "Agence Adidogomé": "route de Kpalimé, en face du camp 2eme RI, Lomé, Togo",
    "Agence Agoè": "Sur la Nationale N°1, en face du Commissariat d’Agoè, Togo",
    "Agence Baguida": "Gendarmerie de Baguida, en face de l’ancienne cité BCEAO, Lomé, Togo",
    "Agence Bè": "Sur la rue Notre Dame des Apôtres, à 200 m du marché côté ouest, Bè, Lomé, Togo",
    "Agence Hédzranawoé": "Sur le Bd du Haho, près du marché, Lomé, Togo",
    "Agence Régionale de Tsévié": "Quartier Atikoumé, à 100 m de la Nationale N°1, Tsévié, Togo",
    "Agence Aného": "Quartier Jéricho, à 500 m de la Frontière Togo-Bénin, Aného, Togo",
    "Agence Tabligbo": "Quartier Afonouvi Komé, à 300 m du Monument de l’Indépendance, Tabligbo, Togo",
    "Agence Vogan": "Quartier Adjrégbo, à 10 m du Commissariat de Vogan, Vogan, Togo",
    "Agence Régionale d’Atakpamé": "Sur la bretelle de l’Evêché, Atakpamé, Togo",
    "Agence Anié": "Quartier Sonitra, immeuble CIB, Anié, Togo",
    "Agence Kpalimé":"Quartier Atakpamé Kondji, sur la route Kpalimé-Atakpamé, à côté de CIB-INTA, Kpalimé, Togo",
    "Agence Notsè": "Quartier Alinou, à côté du marché sur la route Notsé-Agou, Notsè, Togo",
    "Agence Régionale de Sokodé":"Quartier administratif, à côté de l’Hôtel Central, Sokodé, Togo",
    "Agence Bassar":"Quartier administratif, immeuble CIB, Bassar, Togo",
    "Agence Sotouboua":"Quartier Laouwaï, en face de la poste, Sotouboua, Togo",
    "Agence Régionale de Kara": "Quartier Chaminade, en face de la place de la Victoire, Kara, Togo",
    "Agence Kanté": "Quartier Houde, sur la nationale N° 1, Kanté, Togo",
    "Agence Kétao": "Quartier Zongo, à côté de la SAMES, Kétao, Togo",
    "Agence Niamtougou": "Sur la Nationale n° 1 en face de la CEET Niamtougo, Niamtougou, Togo",
    "Agence Pya": "Quartier Pya Towouda, immeuble CIB INTA, Pya, Togo",
    "Agence Guérin-kouka": "A côté de la TDE, Guérin-kouka, Togo",
    "Agence Bafilo": "Quartier Wawande, à côté de la radio la voix d’Assoli, Bafilo, Togo",
    "Agence Régionale de Dapaong": "Quartier Nassablé en face de l’ICAT, Dapaong, Togo",
    "Agence Mango": "Quartier Koko, en face de la gare routière sur la Nationale n°1, Mango, Togo",
    "Agence Cinkassé": "A côté de l’agence Moov, Cinkassé, Togo"
}

branch_data = []
for agence, address in adresses_togo.items():
    latitude, longitude = get_coordinates(address, api_key)
    branch_data.append({
        'Agence': agence,
        'Latitude': latitude,
        'Longitude': longitude
    })
country_data["Togo"] = branch_data

with open('sunu_bank/sunu_bank_togo.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

"""
import json

with open('sunu_bank/sunu_bank_togo.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

sunu_bank_data = []
for country, branches in data.items():
    for branch in branches:
        sunu_bank_data.append({
            "bank": "sunu_bank",
            "country": "togo",
            "address": branch["Agence"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })
with open("result/json_data_all/sunu_bank.json", "w", encoding="utf-8") as f:
    json.dump(sunu_bank_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Togo'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/sunu_bank/sunu_bank_togo.shp')


"""