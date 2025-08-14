
"""
address_af = {
    "Succursale (Ouagadougou)": "479, Avenue Kwamé N’Krumah, Ouagadougou, Burkina Faso",
    "Zone Commerciale (Ouagadougou)": "395, Avenue Loudum, Ouagadougou, Burkina Faso",
    "Gounghin (Ouagadougou)": "Avenue Kadiogo, Ouagadougou, Burkina Faso",
    "Prestige (Ouagadougou)": "479, Avenue Kwamé N’Krumah, Ouagadougou, Burkina Faso",
    "Zogona (Ouagadougou)": "Avenue Babanguida, Ouagadougou, Burkina Faso",
    "Tampouy (Ouagadougou)": "N°142 Avenue Yatenga, Ouagadougou, Burkina Faso",
    "Ouaga 2000 (Ouagadougou)": "Boulevard France Afrique, Ouagadougou, Burkina Faso",
    "Bobo Dioulasso": "510, Rue Dubuc, Bobo-Dioulasso, Burkina Faso",
    "Koudougou": "Nationale n°14, Koudougou, Burkina Faso",
    "Koupéla": "Angle route Fada / Tenkodogo, Koupéla, Burkina Faso",
    "Banfora": "Route Nationale, Banfora, Burkina Faso",
    "Ouahigouya": "Route Nationale, Ouahigouya, Burkina Faso",
    "Dédougou": "Zone Commerciale, Dédougou, Burkina Faso",
    "Pouytenga": "Avenue de la Mairie en face de la Cave Pouya, Pouytenga, Burkina Faso",
    "Tenkodogo": "Route Nationale N°16, Tenkodogo, Burkina Faso"
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
    #truncate the value to keep only the 88 first characters
    lat, lng = get_coordinates(value, api_key)
    data_burkina.append({
        "name": key,
        "address": value[:88],
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"burkina": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/apbef/apbef.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""

import json
with open("burkina/apbef/apbef.json", "r") as f:
    data = json.load(f)

burkina_data=[]
for branch in data["burkina"]:
    burkina_data.append({
        "bank": "vista_bank",
        "country": "burkina",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/apbef_vista_bank.json", "w", encoding="utf-8") as f:
    json.dump(burkina_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['burkina'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/apbef/apbef.shp')

"""
