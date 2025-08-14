"""
address_af = agency_city_dict = {
    "Agence principale": "Niamey, Niamey, Niger",
    "Agence de Maradi": "Maradi, Maradi, Niger",
    "Agence de Dosso": "Dosso, Dosso, Niger",
    "Agence de Magaria": "Magaria, Zinder, Niger",
    "Agence de Téra": "Téra, Tillabéri, Niger",
    "Agence de Doutchi": "Doutchi, Dosso, Niger",
    "Agence de Tahoua": "Tahoua, Tahoua, Niger",
    "Agence de Dakoro": "Dakoro, Maradi, Niger",
    "Agence de Tessaoua": "Tessaoua, Zinder, Niger",
    "Agence de Agadez": "Agadez, Agadez, Niger",
    "Agence de Zinder": "Zinder, Zinder, Niger",
    "Agence de Tillaberi": "Tillabéri, Tillabéri, Niger",
    "Agence de Konni": "Konni, Tahoua, Niger",
    "Agence de Madaoua": "Madaoua, Tahoua, Niger",
    "Agence de Diffa": "Diffa, Diffa, Niger",
    "Agence de Matamey": "Matamey, Tillabéri, Niger",
    "Agence de Gaya": "Gaya, Tillabéri, Niger",
    "Agence Plâteau": "Plateau, Niamey, Niger",
    "Agence Francophonie": "Francophonie, Niamey, Niger",
    "Agence Campus": "Campus, Niamey, Niger",
    "Agence Saga": "Saga, Niamey, Niger",
    "Agence Maourey": "Maourey, Niamey, Niger",
    "Agence Rond point Baré": "Rond Point Baré, Niamey, Niger",
    "Agence Wadata": "Wadata, Niamey, Niger"
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
    
data_all = {"niger": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/bagri/bagri.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("niger/bagri/bagri.json", "r", encoding="utf-8") as f:
    data = json.load(f)

niger_data=[]
for branch in data["niger"]:
    niger_data.append({
        "bank": "bagri",
        "country": "niger",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/bagri.json", "w", encoding="utf-8") as f:
    json.dump(niger_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['niger'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/bagri/bagri_weak.shp')

"""
