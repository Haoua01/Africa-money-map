"""
address_af = {
    "Siège social": "Avenue Tansoba Goalma, Ouagadougou, Burkina Faso",
    "Agence 10 Yaar": "Marché du secteur N° 10, Ouagadougou, Burkina Faso",
    "AGENCE BOBO MARCHE": "Rue Guillaume Ouédraogo, Bobo-Dioulasso, Burkina Faso",
    "Agence Boulevard": "Boulevard Felix Houphet Boigny, Bobo-Dioulasso, Burkina Faso",
    "Agence de Dédougou": "Marché Central, Dédougou, Burkina Faso",
    "Agence Kamboinsin": "Kamboinsin, Ouagadougou, Burkina Faso",
    "Agence Kilwin": "Avenue du Yatenga, Kilwin, Ouagadougou, Burkina Faso",
    "Agence Kua": "Kua, Bobo-Dioulasso, Burkina Faso",
    "Agence Kwamé N’Krumah": "Avenue Kwamé N’Krumah, Ouagadougou, Burkina Faso",
    "Agence Patte d’oie": "Avenue France Afrique, Ouagadougou, Burkina Faso",
    "Agence Pissy": "Rue du Marché, Ouagadougou, Burkina Faso",
    "Agence Prestige": "Rue de l’hôtel de ville, Ouagadougou, Burkina Faso",
    "Agence Zogona": "Avenue Charles de Gaulle, Ouagadougou, Burkina Faso",
    "Koudougou": "Zone commerciale - Marché Central (RN 14 en face de la station SKI), Koudougou, Burkina Faso",
    "Ouahigouya": "Avenue de Mopti BP 358 Ouahigouya, Ouahigouya, Burkina Faso",
    "Tenkodogo": "RN.16 01 BP 99 Tenkodogo, Tenkodogo, Burkina Faso"
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
        "address": value[:50],
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"burkina": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/ib-bank/ib.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("burkina/ib-bank/ib.json", "r", encoding='utf-8') as f:
    data = json.load(f)

burkina_data=[]
for branch in data["burkina"]:
    burkina_data.append({
        "bank": "ib_bank",
        "country": "burkina",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/ib_bank.json", "w", encoding='utf-8') as f:
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

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/ib-bank/ib-bank-burkina.shp')

"""
