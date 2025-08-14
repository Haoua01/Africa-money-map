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


# Replace with the actual URL you want to scrape
url = 'https://www.biat.tg/index.php/notre-reseau' 

# Send a GET request to fetch the raw HTML content
response = requests.get(url,verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to hold the extracted data
    branches_data = []

    # Find all the sections containing branch details
    sections = soup.find_all('div', class_='sppb-addon-text-block')

    # Extract data for each branch
    for section in sections:
        branch_info = section.find('div', class_='sppb-addon-content')
        if branch_info:
            # Extract text from <p> tags
            paragraphs = branch_info.find_all('p')
            if len(paragraphs) >= 1:
                # Extracting the address and contact numbers
                branch_address = paragraphs[0].get_text(strip=True)
                contact_numbers = paragraphs[-1].get_text(strip=True)
                address_raw = branch_address.split(':')[1].strip()
                cleaned_address = re.sub(r'(BP|B\.P\.)\s*\d+', ' ', address_raw).strip()     
                address = re.sub(r'\(\+228\)\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}(\(\+228\)\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2})*', '', cleaned_address).strip()
   
                latitute, longitude = get_coordinates(address, api_key)

                branches_data.append({
                    "Branch": branch_address.split(':')[0].strip(),
                    "Latitude": latitute,
                    "Longitude": longitude
                })


    country_data["Togo"] = branches_data

    # Save the data to a JSON file
    with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/bia_togo.json', 'w', encoding='utf-8') as json_file:
        json.dump(country_data, json_file, ensure_ascii=False, indent=4)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

"""
import json
with open('cbao/bia_togo_corrected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

import pandas as pd

for country, country_info in data.items():
    data_branches = []
    for branch in country_info:
        data_branches.append({
            "bank": "bia",
            "country": "togo",
            "address": branch["Branch"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 0
        })

df = pd.DataFrame(data_branches)
with open('result/json_data_all/bia.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

"""
# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['Togo'])

#limit df['Branch'] to 88 characters
df['Branch'] = df['Branch'].str.slice(0, 88)


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/cbao/bia.shp')

"""
