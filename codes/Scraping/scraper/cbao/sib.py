"""
address_sib = {
    "Abobo 1": "Agence SIB Abobo Cote d'Ivoire",
    "Abobo 2": "Agence SIB Plateau-Dokui, Abobo, Cote d'Ivoire",
    "Adjamé 1": "Agence SIB Adjamé 220 Logements Cote d'Ivoire",
    "Adjamé 2": "Agence SIB Adjamé Forum Cote d'Ivoire",
    "Attécoubé": "Agence SIB ATTECOUBE Cote d'Ivoire",
    "Grand-Bassam": "Agence SIB Grand-Bassam Cote d'Ivoire",
    "Koumassi 1": "Agence SIB Koumassi Pangolin Cote d'Ivoire",
    "Koumassi 2": "Agence SIB Koumassi Cote d'Ivoire",
    "Marcory 1": "Agence SIB Marcory Marché Cote d'Ivoire",
    "Marcory 2": "Agence SIB Marcory Ste Thérèse Cote d'Ivoire",
    "Marcory 3": "Agence SIB Marcory Pierre & Marie Curie Cote d'Ivoire",
    "Marcory 4": "Agence SIB Boulevard de Marseille Cote d'Ivoire",
    "Marcory 5": "Agence SIB Marcory Cote d'Ivoire",
    "Marcory 6": "Agence SIB VGE Cote d'Ivoire",
    "Marcory 7": "Agence SIB Marcory Square Center Cote d'Ivoire",
    "Plateau 1": "Agence Espace Privilège Rue des Jardins Cote d'Ivoire",
    "Plateau 2": "Agence SIB Centre Commercial Djibi Cote d'Ivoire",
    "Plateau 3": "Agence SIB Cocody Boulevard de France Cote d'Ivoire",
    "Plateau 4": "Agence SIB Cocody Palm Club Cote d'Ivoire",
    "Plateau 5": "Agence SIB 2 Plateaux Cote d'Ivoire",
    "Plateau 6": "Agence SIB Angré Djibi Cote d'Ivoire",
    "Plateau 7": "Agence SIB Angré Les Oscars Cote d'Ivoire",
    "Plateau 8": "Agence SIB Boulevard Latrille Cote d'Ivoire",
    "Plateau 9": "Agence SIB Carrefour Abatta Cote d'Ivoire",
    "Plateau 10": "Agence SIB Cocody Cote d'Ivoire",
    "Plateau 11": "Agence SIB Cocody Corniche Cote d'Ivoire",
    "Plateau 12": "Agence SIB Palmeraie Cote d'Ivoire",
    "Plateau 13": "Agence SIB Riviera 3 Cote d'Ivoire",
    "Plateau 14": "Agence SIB Riviera 2 Cote d'Ivoire",
    "Plateau 15": "Agence Agence Centrale Cote d'Ivoire",
    "Plateau 16": "Agence Agence Diplomatique Cote d'Ivoire",
    "Plateau 17": "Agence SIB Avenue Noguès Cote d'Ivoire",
    "Plateau 18": "Agence SIB 2000 Cote d'Ivoire",
    "Plateau 19": "Agence SIB Commerce Cote d'Ivoire",
    "Plateau 20": "Agence SIB Plateau Harmonie Cote d'Ivoire",
    "Port-Bouet": "Agence SIB Vridi Palm Beach Cote d'Ivoire",
    "Treichville 1": "Agence SIB Palais des Sports Treichville Cote d'Ivoire",
    "Treichville 2": "Agence SIB Treichville Avenue 8 Cote d'Ivoire",
    "Treichville 3": "Agence SIB Treichville Nouveau Marché Cote d'Ivoire",
    "Treichville 4": "Agence SIB Zone 3 SOCOPRIX Treichville Cote d'Ivoire",
    "Yopougon 1": "Agence SIB Yopougon 1er Pont Cote d'Ivoire",
    "Yopougon 2": "Agence SIB Yopougon Base CIE Cote d'Ivoire",
    "Yopougon 3": "Agence SIB Yopougon Nouveau Quartier Cote d'Ivoire",
    "Yopougon 4": "Agence SIB Yopougon Quartier Maroc Cote d'Ivoire",
    "Yopougon 5": "Agence SIB Yopougon Siporex Cote d'Ivoire"
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
for key, value in address_sib.items():
    lat, lng = get_coordinates(value, api_key)
    data_civ.append({
        "name": key,
        "address": value,
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"cotedivoire": data_civ}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/sib.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("cbao/sib.json", "r") as f:
    data = json.load(f)

civ_data=[]

for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "sib",
        "country": "civ",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })



with open("result/json_data_all/sib.json", "w", encoding="utf-8") as f:
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

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/sib.shp')


"""