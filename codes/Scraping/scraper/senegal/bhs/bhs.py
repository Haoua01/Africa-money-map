"""
import requests
from bs4 import BeautifulSoup
import json

from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
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


# Sample HTML string (replace this with the actual content you are scraping)
html_file = "/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bhs/bhs.html"

# Load the HTML content
with open(html_file, 'r') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the agency details
agencies = []

# Iterate over each agency entry in the HTML
for agency_div in soup.find_all('div', class_='panel-panel panel-col'):
    # Extract agency name
    name = agency_div.find('h2')
    name = name.text.strip() if name else 'N/A'
    
    # Extract address
    address = agency_div.find('div', class_='field-name-field-adresse-agence')
    address = address.text.strip() if address else 'N/A'
    
    # Extract phone number
    phone = agency_div.find('div', class_='field-name-field-telephone')
    phone = phone.text.strip() if phone else 'N/A'
    
    # Extract location
    location = agency_div.find('div', class_='field-name-field-localisation')
    location = location.text.strip() if location else 'N/A'

    adress_and_location = address + ", " + location
    # Get the coordinates for the agency
    latitude, longitude = get_coordinates(adress_and_location, api_key)
    
    # Append the agency details to the list
    agencies.append({
        'Name': name,
        'Address': address,
        'Phone': phone,
        "Latitude": latitude,
        "Longitude": longitude,
    })

# Print the extracted details
for agency in agencies:
    print(f"Name: {agency['Name']}")
    print(f"Latitude: {agency['Latitude']}")
    print(f"Longitude: {agency['Longitude']}")

bhs_data = {}
bhs_data["Senegal"] = agencies

# Save the data to a JSON file
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bhs/bhs.json', 'w', encoding='utf-8') as json_file:
    json.dump(bhs_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
"""
import json
with open('senegal/bhs/bhs_corrected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

senegal_data = []
for branch in data["Senegal"]:
    senegal_data.append({
        "bank": "bhs",
        "country": "senegal",
        "address": branch["Address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 1
    })

with open('result/json_data_all/bhs.json', 'w', encoding='utf-8') as f:
    json.dump(senegal_data, f, ensure_ascii=False, indent=4)
"""
import pandas as pd
# Convert the JSON data to a DataFrame

df = pd.DataFrame(data['Senegal'])


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/senegal/bhs/bhs.shp')"""