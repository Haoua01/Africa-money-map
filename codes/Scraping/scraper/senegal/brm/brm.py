
"""import requests
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


adress_brm = {"BRM Asset Management": "Immeuble la rotonde, Rue Dr Thèze X Assane NDOYE, Dakar, Sénégal",
              "BRM OPI": "Immeuble la rotonde, Rue Dr Thèze X Assane NDOYE, Dakar, Sénégal"}

data_senegal = []
for key, value in adress_brm.items():
    lat, lng = get_coordinates(value, api_key)
    data_senegal.append({
        "name": key,
        "address": value,
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"Senegal": data_senegal}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/brm/brm.json", "w") as f:
    json.dump(data_all, f, indent=4)

print("Fichier JSON généré avec succès !")
"""
import json
with open("senegal/brm/brm.json", "r") as f:
    data = json.load(f)

senegal_data=[]
for branch in data["Senegal"]:
    senegal_data.append({
        "bank": "brm",
        "country": "senegal",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/brm_senegal.json", "w", encoding="utf-8") as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Senegal'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/brm/brm.shp')


"""