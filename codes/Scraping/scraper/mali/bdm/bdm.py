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


# Initialize an empty list to store the data
agencies =[
  {
    "name": "Agence Principale 1",
    "address": "Quartier du fleuve, 525 Av. Modibo Keïta, Bamako - Mali"
  },
  {
    "name": "Agence Principale II",
    "address": "Centre-ville, Avenue Modibo Keïta, Bamako - Mali"
  },
  {
    "name": "Agence Boubacar SIDIBE",
    "address": "Bamako-coura, Rue Elhadj Ousmane, Bamako - Mali"
  },
  {
    "name": "Agence de Badalabougou SEMA GEXCO",
    "address": "Rue 136 porte 778, Bamako - Mali"
  },
  {
    "name": "Agence de Djicoroni Para",
    "address": "Près Institut Marchoux, Bamako - Mali"
  },
  {
    "name": "Agence de Korofina",
    "address": "Route de Koulikoro, Bamako - Mali"
  },
  {
    "name": "Agence de Quinzambougou",
    "address": "Rue Achkhabad, Bamako - Mali"
  },
  {
    "name": "Agence de Ngolonina",
    "address": "Imm. A. SYLLA, Bamako - Mali"
  },
  {
    "name": "Agence de Bagadadji",
    "address": "Ex-cinéma RIO face A.N., Bamako - Mali"
  },
  {
    "name": "Agence de Baco-Djicoroni",
    "address": "Route de Kalabancoro - Imm. Alou Kouma, Bamako - Mali"
  },
  {
    "name": "Agence de Lafiabougou",
    "address": "Av. cheick Zayed - Imm. Adama Baye Sissako, Bamako - Mali"
  },
  {
    "name": "Agence A.C.I. 2000",
    "address": "Hôtel Radisson - A.C.I. 2000 Hamdallaye, Bamako - Mali"
  },
  {
    "name": "Agence de Sogoniko",
    "address": "Avenue de L’OUA - Sogoniko, Bamako - Mali"
  },
  {
    "name": "Agence de Yirimadio",
    "address": "Yirimadio Route Nationale axe Bamako-Segou, Bamako - Mali"
  },
  {
    "name": "Agence de Badalabougou",
    "address": "Imm. Azar Center, Bamako - Mali"
  },
  {
    "name": "Agence de Torokorobougou",
    "address": "Rue 427 près du quick shop, Bamako - Mali"
  },
  {
    "name": "Agence de Missira",
    "address": "Rue Achkhabad non loin de la Mairie, Bamako - Mali"
  },
  {
    "name": "Bureau Minusma",
    "address": "Sénou, Route de l’aéroport, Bamako - Mali"
  },
  {
    "name": "Agence de Sebenikoro",
    "address": "Face hopital Militaire, Bamako - Mali"
  },
  {
    "name": "Agence de Sotuba",
    "address": "Sotuba, Bamako - Mali"
  },
  {
    "name": "Agence Dramane Diakité",
    "address": "Bamako - Mali"
  },
  {
    "name": "Agence de Kalaban Coura",
    "address": "Route de l'aéroport, Bamako - Mali"
  },
  {
    "name": "Agence Dibida",
    "address": "Marché Dibidani, Bamako - Mali"
  },
  {
    "name": "Agence PME PMI",
    "address": "En face de BOUGIBA, Bamako - Mali"
  },
  {
    "name": "Agence de Kabala",
    "address": "Face à l'université, Bamako - Mali"
  },
  {
    "name": "Agence de Magnambougou",
    "address": "Tournant de Magnambougou, Bamako - Mali"
  },
  {
    "name": "Agence de Boulkassoumbougou",
    "address": "Immeuble SODOUF, Bamako - Mali"
  },
  {
    "name": "Agence de Kati",
    "address": "En face de la Mairie, Kati - Mali"
  },
  {
    "name": "Agence de Koulikoro",
    "address": "Gare face Dir. Régionale Agriculture, Koulikoro - Mali"
  },
  {
    "name": "Agence de Ségou 1",
    "address": "Route Nationale 6, Ségou - Mali"
  },
  {
    "name": "Agence de Ségou 2",
    "address": "Quartier Commercial, Ségou - Mali"
  },
  {
    "name": "Agence de Sikasso 1",
    "address": "Centre commercial Kaboila I, Sikasso - Mali"
  },
  {
    "name": "Agence de Sikasso 2",
    "address": "Immeuble La Sikassoise Kaboila I, Sikasso - Mali"
  },
  {
    "name": "Agence de Fourou",
    "address": "Cercle de Kadiolo, Cité ouvrière, Fourou - Mali"
  },
  {
    "name": "Agence de San",
    "address": "Route Nationale n° 6 Médine, San - Mali"
  },
  {
    "name": "Agence de Niono",
    "address": "Quartier Administratif, Niono - Mali"
  },
  {
    "name": "Agence de Nioro du Sahel",
    "address": "Centre Commercial - Quartier Diaka, Nioro du Sahel - Mali"
  },
  {
    "name": "Agence de Yelimané",
    "address": "Près de Station Sahel, Yelimané - Mali"
  },
  {
    "name": "Agence de Manantali",
    "address": "Cité des cadres, Manantali - Mali"
  },
  {
    "name": "Agence de Kita",
    "address": "Centre Commercial, Kita - Mali"
  },
  {
    "name": "Agence de Touba",
    "address": "Quartier Administratif, Touba - Mali"
  },
  {
    "name": "Agence de Banamba",
    "address": "Marché de Banamba, Banamba - Mali"
  },
  {
    "name": "Agence de Mopti",
    "address": "Komoguel 2 Centre Comm. - BP 42 bld Indép, Mopti - Mali"
  },
  {
    "name": "Agence de Tombouctou",
    "address": "Sans fils, route de Kabara, Tombouctou - Mali"
  },
  {
    "name": "Agence de Gao",
    "address": "Quartier Dioulabougou, Gao - Mali"
  },
  {
    "name": "Agence de Kayes 1",
    "address": "Quartier Liberté, Kayes - Mali"
  },
  {
    "name": "Agence de Kayes 2",
    "address": "Grand marché, Kayes - Mali"
  },
  {
    "name": "Agence de Diéma",
    "address": "Immeuble Brehima Diawara, Quartier Razel, Diéma - Mali"
  },
  {
    "name": "Agence de Nara",
    "address": "Nara Liberté, Quartier Météo, Nara - Mali"
  },
  {
    "name": "Agence de Koutiala",
    "address": "1er Quartier du Centre Commercial, Koutiala - Mali"
  },
  {
    "name": "Agence de Kéniéba",
    "address": "Marché de Kéniéba, Kéniéba - Mali"
  },
  {
    "name": "Agence de Yanfolila",
    "address": "Près de la Poste, Yanfolila - Mali"
  },
  {
    "name": "Agence de Sévaré",
    "address": "Sevare Centre Commercial, Sévaré - Mali"
  },
  {
    "name": "Agence de Mahina",
    "address": "1er Quartier Face à la Grande Mosquée, Mahina - Mali"
  },
  {
    "name": "Agence de Fana",
    "address": "Route de Ségou RN6 face à l'EDM, Fana - Mali"
  },
  {
    "name": "Agence de Mbewani",
    "address": "Usine NSUKALA, Mbewani - Mali"
  },
  {
    "name": "Agence de Bougouni",
    "address": "Bougouni - Mali"
  },
  {
    "name": "Agence de DIO",
    "address": "Usine Diamond Ciment, DIO - Mali"
  }
]




for agency in agencies:
    lat, lng = get_coordinates(agency["address"], api_key)
    agency["Latitude"] = lat
    agency["Longitude"] = lng




country_data={}
country_data["mali"]=agencies

# Save the data to a JSON file
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/mali/bdm/bdm.json', 'w') as f:
    json.dump(country_data, f, indent=4)
"""
import json
# Read the JSON file
with open('mali/bdm/bdm.json', 'r') as f:
    data = json.load(f)

mali_data = []
for branch in data["mali"]:
    mali_data.append({
        "bank": "bdm",
        "country": "mali",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/bdm_mali.json", "w", encoding='utf-8') as f:
    json.dump(mali_data, f, indent=4)

"""
import pandas as pd

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mali'])

# Save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/mali/bdm/bdm_geocoded.shp')"""