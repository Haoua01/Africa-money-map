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
    "name": "Agence Principale",
    "address": "Avenue de la Mairie, Niamey - Niger",
    "telephone": "(227) 20 73 31 01 / 02"
  },
  {
    "name": "Agence Grand marché",
    "address": "Route du Balafon, Niamey - Niger",
    "telephone": "(227) 20 73 24 64"
  },
  {
    "name": "Agence Kalley sud",
    "address": "Immeuble Bague Daouada, Niamey - Niger",
    "telephone": "(227) 20 74 34 17"
  },
  {
    "name": "Agence Boukoki",
    "address": "Boulevard de de l’Independance, Niamey - Niger",
    "telephone": "(227) 85 86 92 09"
  },
  {
    "name": "Agence Plateau",
    "address": "Avenue Maurice Delens, Niamey - Niger",
    "telephone": "(227) 20 35 10 36"
  },
  {
    "name": "Agence Rive droite",
    "address": "Rue du Gourma, Niamey - Niger",
    "telephone": "(227) 21 73 22 90"
  },
  {
    "name": "Agence Wadata",
    "address": "Arène de Lutte Traditionelle, Niamey - Niger",
    "telephone": "(227) 20 74 18 73"
  },
  {
    "name": "Agence Yantala",
    "address": "Rond Point Gadafawa, Niamey - Niger",
    "telephone": "(227) 20 35 03 53"
  },
  {
    "name": "Agence Agadez",
    "address": "Marché des Tôles, Agadez - Niger",
    "telephone": "(227) 20 44 04 05"
  },
  {
    "name": "Agence Arlit",
    "address": "Route Zone Industrielelle de la somaïr, Arlit - Niger",
    "telephone": "(227) 20 45 22 22"
  },
  {
    "name": "Agence Diffa",
    "address": "Quartier Administratif, Diffa - Niger",
    "telephone": "(227) 20 54 03 06"
  },
  {
    "name": "Agence Dosso",
    "address": "Quartier Mague koira, Dosso - Niger",
    "telephone": "(227) 20 65 08 67"
  },
  {
    "name": "Agence Gaya",
    "address": "Quartier Plateau, Gaya - Niger",
    "telephone": "(227) 20 68 04 90"
  },
  {
    "name": "Agence Konni",
    "address": "Centre Commercial, Konni - Niger",
    "telephone": "(227) 20 64 07 17"
  },
  {
    "name": "Agence Maradi",
    "address": "Quartier Mokoyo, Maradi - Niger",
    "telephone": "(227) 20 41 02 42"
  },
  {
    "name": "Agence Tahoua",
    "address": "Quartier zoulanké, Tahoua - Niger",
    "telephone": "(227) 20 61 00 91"
  },
  {
    "agence": "Agence Zinder",
    "address": "La Poste, Zinder - Niger",
    "telephone": "(227) 20 51 0024"
  }
]


for agency in agencies:
    lat, lng = get_coordinates(agency["address"], api_key)
    agency["Latitude"] = lat
    agency["Longitude"] = lng




country_data={}
country_data["niger"]=agencies

# Save the data to a JSON file
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/bsic/Geocoding/bsic_all_v2.json', 'w') as f:
    json.dump(country_data, f, indent=4)

"""
# Read the JSON file
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/bsic/Geocoding/bsic_all_v2.json', 'r') as f:
    data = json.load(f)

import pandas as pd

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['niger'])

# Save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/niger/bia/bia_geocoded.shp')
"""