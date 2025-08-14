"""address_bcici = {
    "PLATEAU SIEGE": "01 BP 1298 Avenue Franchet d'Espérey, Plateau",
    "MARCORY PLAYCE": "BP 1298 Centre commercial Cfao carrefour boulevard VGE, Marcory",
    "YOPOUGON KENEYA": "BP 1298 Rue principale, Yopougon",
    "YAMOUSSOUKRO": "BP 97 Route d'Abidjan, Yamoussoukro",
    "VRIDI": "Rue des Pétroliers Zone industrielle, Vridi",
    "TREICHVILLE MARCHE": "Rue 12, Treichville",
    "SOUBRE": "BP 252 Avenue principale, carrefour Dobois, Soubré",
    "CAP NORD": "Centre commercial Cap Nord cocody Rivièra-Allabra, Cocody",
    "PORT-BOUET": "Avenue de l'Océan, Port-Bouet",
    "MARIE CURIE ZONE 4": "Zone 4 - Rdc immeuble Marie Curie, Marcory",
    "II PLATEAUX LATRILLE": "BP 0722 Face Commisariat Angré Rdc Imm SIL 07, Cocody",
    "Koumassi 7 décembre": "Bd du 7 décembre, Koumassi",
    "KORHOGO": "BP 66 korhogo Rue Principale, Korhogo",
    "GAGNOA": "Bp 587 Rue du commerce, Gagnoa",
    "DJIBI": "Carrefour Nelson Mandela, Cocody",
    "PLATEAU RUE DU COMMERCE": "Avenue Nogues Résidence Nabil, Plateau",
    "II PLATEAU VALLON": "1298 Rue des Jardins II Plateaux vallons face Super Hayat, Cocody",
    "PLATEAU CLOZEL": "20/22 Bd Clozel Résidence Les Acacias, Plateau",
    "CITE DES ARTS": "Cocody Cité des Arts, Cocody",
    "89 BD DE MARSEILLE ABIDJAN": "89 Bd de Marseille, Marcory",
    "BOUAKE": "BP 583 Bd de la Mairie Quartier de commerce, Bouaké",
    "TREICHVILLE ARRAS": "Avenue Laurent Pierre Clouzet, Treichville",
    "ADJAME": "Bd Nagui Abrogoua, Adjamé",
    "ABOBO": "Quatier Amakébou face CI Télécom, Abobo",
    "ROND POINT PALMERAIE": "01 BP 1298 Avenue Franchet d'Espérey, Plateau",
    "ABENGOUROU": "BP 139 Abengourou- Place du marché, Abengourou",
    "YOPOUGON NIANGON": "Niangon base CIE, carrefour menuisierie, Yopougon",
    "ZONE INDUSTRIELLE YOPOUGON": "Zone indistruelle, Yopougon",
    "MARCORY REMBLAIS": "Quartier remblais (marché marcory), Marcory",
    "GRAND BASSAM": "Quartier cafop II- route de Moossou, Grand-Bassam",
    "RIVIERA GOLF": "Centre commercial SICOGI, Yopougon",
    "SAN PEDRO": "Bp 335 Bd de la République Quartier cité San Pedro, San-Pédro",
    "INP-HB YAMOUSSOUKRO": "Yamoussoukro, Yamoussoukro"
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
for key, value in address_bcici.items():
    lat, lng = get_coordinates(value, api_key)
    data_civ.append({
        "name": key,
        "address": value,
        "Latitude": lat, 
        "Longitude": lng})
    
data_all = {"cotedivoire": data_civ}

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bcici/bcici.json", "w") as f:
    json.dump(data_all, f, indent=4)
"""

import json
with open("civ/bcici/bcici.json", "r", encoding="utf-8") as f:
    data = json.load(f)

civ_data=[]
for branch in data["cotedivoire"]:
    civ_data.append({
        "bank": "bicici",
        "country": "civ",
        "address": branch["address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open("result/json_data_all/bicici.json", "w", encoding="utf-8") as f:
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

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bcici/bcici.shp')


"""