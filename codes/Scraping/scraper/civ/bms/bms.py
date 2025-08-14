"""address_af = {
    "Agence Principale": "Abidjan plateau à l’angle de la rue Paris-village et de l’avenue Botreau Roussel, près de la Radio NOSTALGIE, 16 BP 114 Abidjan 16",
    "Agence du Plateau": "Abidjan plateau rue du commerce, siège à l’immeuble du MALI, Cote d'Ivoire",
    "Agence de Port-Bouët": "Abidjan PORT-BOUET sur le prolongement du centre pilote, face au parc à bétail",
    "Agence d’Adjamé": "Abidjan Adjamé, rue des banques face au marché forum, ancienne poste des télécommunications",
    "Agence de Bouaké": "BOUAKE quartier DJAMBOUROU après le marché de gros, sur l’autoroute menant à KATIOLA",
    "Agence de Korhogo": "Korhogo, quartier Koko, Gare Léopard, Côte d’Ivoire",
    "Agence de San Pedro": "San Pedro au quartier SOTRES en face de la Boulangerie de la paix",
    "Agence de Treichville": "Avenue 16, rue 21, en face de la Station Petro Ivoire, Treichville, Cote d'Ivoire",
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

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bms/bms.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("civ/bms/bms.json", "r", encoding="utf-8") as f:
    data = json.load(f)

civ_data = []
for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "bms",
        "country": "civ",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/bms_civ.json", "w") as f:
    json.dump(civ_data, f, indent=4)


"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['cotedivoire'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bms/bms-civ.shp')

"""
