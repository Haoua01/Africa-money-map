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

branch_data=[]
country_data={}

agences={"Agence Principale": "14 Avenue Sylvanus Olympio, Grand Marché – Assigamé, Lomé, Togo",
"Agence Agbalepedogan":	"station Sanol, Carrefour Bodjona, Adidoadin, Togo",
"Agence Zoro Bar":"Ahadji Kpota (Port), Lomé, Togo"}

for agence, address in agences.items():
    lat, lng = get_coordinates(address, api_key)
    branch_data.append({"address": address, "Latitude": lat, "Longitude": lng})
country_data["Togo"]=branch_data


with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/siab/siab_togo.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)


"""
import json
with open('siab/siab_togo.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

togo_data=[]
for country, branches in data.items():
    for branch in branches:
        togo_data.append({
            "bank": "siab",
            "country": country,
            "address": branch["address"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })

with open("result/json_data_all/siab.json", "w", encoding="utf-8") as f:
    json.dump(togo_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Togo'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/siab/siab_togo.shp')



"""