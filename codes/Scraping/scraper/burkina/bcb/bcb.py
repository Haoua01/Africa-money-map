"""
address_af = {
    "Agence NATION": "800, Avenue de la nation, Ouagadougou, Burkina Faso",
    "Agence Kwamé N'Krumah": "1226, Avenue du Dr Kwamé N'Krumah, Ouagadougou, Burkina Faso",
    "Agence Wayalghin": "Route de Fada, face SONACOF, Ouagadougou, Burkina Faso",
    "Agence Wemtenga": "RUE 29.13 WEMTNGA, Ouagadougou, Burkina Faso",
    "Agence Siège": "653, Avenue du Dr Kwamé N'Krumah 800, Avenue de la nation Ouagadougou, Burkina Faso",
    "Agence Pissy": "Route de Bobo, Face à la Mairie de Boulmiougou, Ouagadougou, Burkina Faso",
    "Agence patte d'Oie": "Face Ouaga inter, Ouagadougou, Burkina Faso",
    "Guichet Grand Marché": "Face au restaurant Eau Vive, Ouagadougou, Burkina Faso",
    "Agence Tampouy": "Route de Ouahigouya, 400m après les rails, Ouagadougou, Burkina Faso",
    "Agence de Belle Ville": "Rue NEZIEN BEDEMBIE, Ouagadougou, Burkina Faso",
    "Agence Balkuy": "Balkuy, Ouagadougou, Burkina Faso",
    "Agence Kossoghin": "Kossoghin, Ouagadougou, Burkina Faso",
    "Agence TENKODOGO": "Côté Est du grand marché, Bâtiment de Faso yaar, Tenkodogo, Burkina Faso",
    "Agence BOBO-DIOULASSO": "Avenue Guillaume Ouedraogo, Bobo-Dioulasso, Burkina Faso",
    "Agence GARANGO": "A l'entrée du grand marché, Garango, Burkina Faso",
    "Agence DORI": "A 20 mètres du Monument Hama Arba DIALLO, Dori, Burkina Faso",
    "Agence KOUDOUGOU": "Avenue Dreux, Koudougou, Burkina Faso",
    "Agence KAYA": "Kaya, Burkina Faso",
    "Agence PO": "Po, Burkina Faso",
    "Agence GAOUA": "Route de la grande gare, Gaoua, Burkina Faso",
    "Agence ORODARA": "Face au marché central Orodara, Burkina Faso",
    "Guichet BOBO MARCHE": "Enceinte du marché de Bobo, Bobo-Dioulasso, Burkina Faso",
    "Agence Boromo": "Boromo, Burkina Faso",
    "Agence OUAHIGOUYA": "01 BP Avenue de Banfora, Ouahigouya, Burkina Faso",
    "Agence ZINIARE": "Ziniare, Burkina Faso",
    "Agence KUA BOBO2": "Bobo-Dioulasso, Burkina Faso",
    "Agence KOUDOUGOU2": "Koudougou, Burkina Faso"
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
    
data_all = {"burkina": data_burkina}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/bcb/bcb.json", "w") as f:
    json.dump(data_all, f, indent=4)

    """
import json
with open("burkina/bcb/bcb.json", "r") as f:
    data = json.load(f)

burkina_data=[]
for branch in data["burkina"]:
    burkina_data.append({
        "bank": "bcb",
        "country": "burkina",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

# Save the data to a JSON file
with open('result/json_data_all/bcb.json', 'w', encoding='utf-8') as f:
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

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/burkina/bcb/bcb.shp')


"""