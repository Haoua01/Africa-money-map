
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

agences = {
    "UTB SGI": "Bvd Gnassingbé Eyadéma, Immeuble SGI non loin de OTR, Lomé, Togo",
    "UTB KWADJOVIAKOPE": "Boulevard du Mono, Immeuble de la Douane, Lomé, Togo",
    "TOTSI": "Fin pavé en allant vers le carrefour LIMOUSINE, Lomé, Togo",
    "UTB - OTR COMMISSARIAT DES IMPÔTS": "Ancien bureau des Impôts face à l’Ambassade des USA, Lomé, Togo",
    "UTB AGENCE CAISSE GUICHET UNIQUE": "Dans l'enceinte de ECOMARINE, Rond point Port, Lomé, Togo",
    "JEAN-PAUL II NOVISSI": "Non loin de la station MRS de Novissi, Lomé, Togo",
    "ADIDOGOME": "Rte Kpalimé face Avé Maria à côté de la pharmacie Béthel, Lomé, Togo",
    "BE KPEHENOU": "Bd H. Boigny à côté de la pharmacie Kpéhénou, Lomé, Togo",
    "CAMPUS": "Bd Kara, Immeuble pharmacie Campus, Lomé, Togo",
    "HEDZRANAWOE": "Face au marché à côté de CIB-INTA, Lomé, Togo",
    "UTB ANEHO": "Bd du Mono à côté de RTDS et de la CNSS, Aného, Togo",
    "UTB ASSAHOUN": "Nationale No 3 (Route de Kpalimé) après le marché, Togo",
    "UTB TSEVIÉ": "Nationale No 1 face à la gendarmerie, Tsévié, Togo",
    "UTB VOGAN": "À côté de la boucherie, Marché de Vogan, Vogan, Togo",
    "UTB TABLIGBO": "À côté de l’immeuble CIB-INTA, Tabligbo, Togo",
    "UTB KPALIMÉ": "Derrière Hôtel de Ville, Kpalimé, Togo",
    "UTB ATAKPAMÉ": "Centre du marché d’Atakpamé, Atakpamé, Togo",
    "UTB ANIÉ": "Nationale No 1, imm. CIB, Anié, Togo",
    "UTB ADETA": "Rte Kpalimé-Amlamé, imm. CIB-INTA, Adeta, Togo",
    "UTB NOTSÉ": "Nationale No 1, imm. Hôtel LUCIA, Notsè, Togo",
    "UTB BLITTA": "Blitta Gare à côté de l'hôpital, Blitta, Togo",
    "UTB SOKODÉ": "Nationale No 1, Rond-point du marché, Sokodé, Togo",
    "UTB SOTOUBOUA": "Nationale No 1, imm. LANDOZ, Sotouboua, Togo",
    "UTB TCHAMBA": "Marché de Tchamba, imm. SAMEX, Tchamba, Togo",
    "UTB KARA": "Face CHU vers le Palais des Congrès, Kara, Togo",
    "UTB KETAO": "Rte Pagouda, imm. CIB derr. Éts. ZAMOU, Kétan, Togo",
    "UTB PYA": "Face BYO Hôtel, Pya, Togo",
    "UTB BASSAR": "Anc. imm. TOGOTÉLÉCOM à côté du stade, Bassar, Togo",
    "UTB GUÉRIN-KOUKA": "Voie Kabou à côté de la Gendarmerie et de la TDE, Guérin-Kouka, Togo",
    "UTB KANTÉ": "Nationale No 1, entre La Poste et CIB-INTA, Kanté, Togo"
}

for agence, address in agences.items():
    lat, lng = get_coordinates(address, api_key)
    branch_data.append({"address": address, "Latitude": lat, "Longitude": lng})
country_data["Togo"]=branch_data


with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/utb/utb_togo.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

"""
import json

with open('utb/utb_togo.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

utb_data=[]
for country, branches in data.items():
    for branch in branches:
        utb_data.append({
            "bank": "utb",
            "country": country,
            "address": branch["address"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })
with open("result/json_data_all/utb.json", "w", encoding="utf-8") as f:
    json.dump(utb_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Togo'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/utb/utb_togo.shp')

"""

