"""
from bs4 import BeautifulSoup
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


# Load the HTML file content
url='https://bis-bank.com/agence-2/'
html_content = requests.get(url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# Find all rows in the table
rows = soup.find_all('tr')[1:]  # Skip the header row

# Initialize a list to store agency details
agencies = []

# Loop through each row and extract data
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 6:
        # Extract each column's content
        agency_name = cols[0].text.strip()
        address = cols[1].text.strip()

        address_full=agency_name + address + ', Senegal'
        lat, lng = get_coordinates(address_full, api_key)

        # Store the data
        agencies.append({
            'Name': agency_name,
            'Address': address,
            'Latitude': lat,
            'Longitude': lng
        })

data_senegal={}
data_senegal["senegal"]=agencies

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bis/bis.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_senegal, json_file, ensure_ascii=False, indent=4)
"""
import json

with open('senegal/bis/bis.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []
for branch in data["senegal"]:
    senegal_data.append({
        "bank": "bis",
        "country": "senegal",
        "address": branch["Address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
with open("result/json_data_all/bis.json", "w", encoding="utf-8") as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['senegal'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bis/bis.shp')
"""

