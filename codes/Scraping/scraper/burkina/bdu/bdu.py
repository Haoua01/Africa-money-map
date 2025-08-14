"""
address_af = {
    "Agence Principale": "Immeuble Abdoulaye TRAORE, rue Loundun 01 secteur 05 Projet ZACA, Ouagadougou, Burkina Faso",
    "Agence SANKARYAARE": "Dapoya, rue KIENDREBEOGO N. Didier, Ouagadougou, Burkina Faso",
    "Agence PISSY": "Immeuble SOBA, route nationale N° 1, Ouagadougou, non loin dela SOLEVO, Burkina Faso",
    "Agence OUAGA 2000": "Immeuble COMPAORE Mouhamed, Ouagadougou, Avnue France-Afrique, Burkina Faso",
    "Agence ZAD": "Immeuble OUEDRAOGO Hamidou, Boulevrd de la circulaire, non loin de la SONABEL, Ouagadougou, Burkina Faso",
    "Agence WAYALGHIN": "Immeuble MANDO Moctar, coté Nord de l'echangeur de l'EST, Ouagadougou, Burkina Faso",
    "Agence CISSIN": "Secteur 25, sur la route du palais de la culture Jean-pierre GUINGANE en face de la SONABEL, Ouagadougou, Burkina Faso",
    "Bureau Kwamé N'Kruma": "Immeuble SODIFA, secteur 05, Ouagadougou, Burkina Faso",
    "Bureau Hamdalaye": "Arrondissement de basky, non loin du marché de 10 yaar, Ouagadougou, Burkina Faso",
    "Bureau Tampouy": "Secteur 16 non loin de la caisse populaire, Ouagadougou, Burkina Faso",
    "Bureau Saaba": "Immeuble ILBOUDO Phillipe, en face du commissariat de SAABA, Ouagadougou, Burkina Faso",
    "Agence BOBO Marché": "Zone commercial, avenue du Gouverneur William PONTY, Bobo-Dioulasso, Burkina Faso",
    "Agence BOBO Boulevard": "A cote du petit marché d'accart ville, Bobo-Dioulasso, Burkina Faso",
    "Agence BOBO Aeroport": "Dans le hall de l'aéroport de Bobo-Dioulasso, Burkina Faso",
    "Agence OUAHIGOUYA": "Sise secteur 08, Face au grand marché, Ouahigouya, Burkina Faso",
    "Agence DEDOUGOU": "Immeuble CAMEG, Dedougou, Burkina Faso",
    "Agence KOUDOUGOU": "Imm. Kiendrebeogo Noraogo, Quartier Zakin secteur 02, Koudougou, Burkina Faso",
    "Agence TENKODOGO": "Imm. Franck Minoungou, Tenkodogo, Burkina Faso",
    "Agence BANFORA": "Immeuble Ouattara Drissa secteur 1, Banfora, Burkina Faso",
    "Agence HOUNDE": "Secteur 4 ,Juste à côté de la mairie, Houndé, Burkina Faso",
    "Agence KAYA": "Immeuble Issaka Korogo, Kaya, Burkina Faso"
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
        "address": value[:88],
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"burkina": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/bdu/bdu.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""
import json
with open("burkina/bdu/bdu.json", "r") as f:
    data = json.load(f)

burkina_data=[]
for branch in data["burkina"]:
    burkina_data.append({
        "bank": "bdu",
        "country": "burkina",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })
with open("result/json_data_all/bdu.json", "w", encoding='utf-8') as f:
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

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/bdu/bdu-burkina.shp')


"""