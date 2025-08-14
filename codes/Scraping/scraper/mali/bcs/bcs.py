"""
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urlparse, parse_qs
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

html_path = '/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bcs/bcs_corrected.html'

# Read the HTML file
with open(html_path, 'r') as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize an empty list to store the data
agency_list = []

# Extract the agency names and other information
for h4_tag in soup.find_all('h4'):
    agency_name = h4_tag.get_text(strip=True)
    address = h4_tag.find_next('p').get_text(strip=True)
    address_full = agency_name + address + ", Mali"
    latitude, longitude = get_coordinates(address_full, api_key)

    
    # Create a dictionary and add it to the list
    agency_dict = {
        "name": agency_name,
        "Latitude": latitude,
        "Longitude": longitude
    }
    agency_list.append(agency_dict)

# Output the list of dictionaries
print(agency_list)

country_data={}
country_data["mali"]=agency_list

# Save the data to a JSON file
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bcs/bcs.json', 'w') as f:
    json.dump(country_data, f, indent=4)
"""
# Read the JSON file
import json
with open('mali/bcs/bcs.json', 'r') as f:
    data = json.load(f)

mali_data = []
for branch in data["mali"]:
    mali_data.append({
        "bank": "bcs",
        "country": "mali",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open('result/json_data_all/bcs.json', 'w', encoding='utf-8') as f:
    json.dump(mali_data, f, indent=4)

"""
import pandas as pd

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mali'])

# Save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bcs/bcs_geocoded.shp')"""