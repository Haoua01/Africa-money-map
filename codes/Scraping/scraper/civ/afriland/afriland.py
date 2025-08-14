"""address_af = {
    "SIEGE SOCIAL ET AGENCE DU PLATEAU": "Avenue Noguès, immeuble Woodin, Plateau, Cote d'Ivoire",
    "AGENCE PRIMA": "Centre commercial Prima Center, Marcory, Zone 4, Cote d'Ivoire",
    "AGENCE DJIBI": "Cité SICOGI Djibi 1, près de Nefco, Cote d'Ivoire",
    "AGENCE DE COCODY Saint Jean": "Centre commercial NGOUAN AKA MATHIAS, Cocody, Cote d'Ivoire",
    "AGENCE DE TREICHVILLE": "En face du grand Marché de Treichville, Cote d'Ivoire",
    "CASH POINT DE TREICHVILLE": "En face du marché de Belle-ville, Treichville, Cote d'Ivoire",
    "AGENCE D’ ADJAME": "Marché Gouro, carrefour Banfora, Adjame, Cote d'Ivoire",
    "AGENCE D’ ABOBO": "En face du Grand marché proche du Collège Moderne d’ Abobo, non loin de la mairie d’Abobo, Cote d'Ivoire",
    "AGENCE D’ ANONO": "Près du marché d’Anono, Cote d'Ivoire",
    "AGENCE DE YOPOUGON": "Carrefour Bel Air, Yopougon, Cote d'Ivoire",
    "AGENCE DE KORHOGO": "En face du marché près de la pharmacie du marché, Korhogo, Cote d'Ivoire",
    "AGENCE DE SAN PEDRO": "Marché de Bardot, San Pedro, Cote d'Ivoire"
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




data_civ = []
for key, value in address_af.items():
    lat, lng = get_coordinates(value, api_key)
    data_civ.append({
        "name": key,
        "address": value[:88],
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"cotedivoire": data_civ}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/afriland/afriland.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("civ/afriland/afriland.json", "r") as f:
    data = json.load(f)

civ_data=[]
for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "afriland_first_bank",
        "country": "civ",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/afriland_first_bank.json", "w", encoding="utf-8") as f:
    json.dump(civ_data, f, ensure_ascii=False, indent=4)


"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['cotedivoire'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/afriland/afriland.shp')

"""
