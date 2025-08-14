
"""
address_af = {
    "Agence Principale": "Av Domingos Ramos N° 33 – Bissau, Guinée-Bissau",
    "Agence Bissau 2": "Central – Bissau, Guinée-Bissau",
    "Agence Bissau 3": "Che Guevara – Bissau, Guinée-Bissau",
    "Agence Bissau 4": "CMB – Bissau, Guinée-Bissau",
    "Agence Bissau 5": "Luanda, Guinée-Bissau",
    "Agence Bissau 6": "Sao Paulo, Bissau, Guinée-Bissau",
    "Agence Bissau 7": "Bra, Bissau, Guinée-Bissau",
    "Agence Bandim": "Av. Combatentes Liberdade da Pátria – Bissau, Guinée-Bissau",
    "Agence Gabu": "Gabu, Guinée-Bissau",
    "Agence Bafata": "Bafata, Guinée-Bissau",
    "Agence Canchungo": "Canchungo, Guinée-Bissau",
    "Agence Buba": "Buba, Guinée-Bissau",
    "Agence Safim": "Safim, Guinée-Bissau",
    "Agence Sao Domingos": "Sao Domingos, Guinée-Bissau",
    "Agence Bantandjan": "Bantandjan, Guinée-Bissau",
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




data_guinee = []
for key, value in address_af.items():
    lat, lng = get_coordinates(value, api_key)
    data_guinee.append({
        "name": key,
        "address": value,
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"guinee": data_guinee}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/guinee-bissau/bao/bao.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("guinee-bissau/bao/bao.json", "r", encoding="utf-8") as f:
    data = json.load(f)

guinee_data=[]
for branch in data["guinee"]:
    guinee_data.append({
        "bank": "bao",
        "country": "guinee",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/bao.json", "w", encoding="utf-8") as f:
    json.dump(guinee_data, f, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['guinee'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/guinee-bissau/bao/bao-guinee.shp')

"""
