from bs4 import BeautifulSoup
import requests
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



# Read the HTML content from the file
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_benin.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

branch_containers=soup.find_all('article', class_="struct anim-scroll anim-from-bottom shadow relative bg-gray flex col w100 vt-40 padding-40 radius-20")

benin_data={}
branch_data = []
for branch in branch_containers:
    agency_name = branch.find("h2", class_="h5 semibold success").text.strip()
    city = branch.find("span", class_="left-20").text.strip()
    address = branch.find_all("div", class_="flex row left middle vt-5-in")[1].find("span", class_="left-20").text.strip()
    address_full = address + ", " + city + ", Benin"
    
    # Find the Google Maps link, check if it exists
    maps_link_tag = branch.find("a", href=True, title="Localiser avec Google Maps")
    
    if maps_link_tag:
        maps_link = maps_link_tag["href"]
        
        # Parse the Google Maps link to extract coordinates
        parsed_url = urlparse(maps_link)
        query_params = parse_qs(parsed_url.query)
        coordinates = query_params.get('q', [None])[0]
        
        # If coordinates are found, split them into latitude and longitude
        latitude, longitude = None, None
        if coordinates:
            try:
                latitude, longitude = coordinates.split('°,')
                longitude = longitude.strip('°')
                #convert to float
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                print("Error parsing coordinates")
    else:
        maps_link = None
        latitude, longitude = get_coordinates(address_full, api_key)

    # Create a dictionary to hold the extracted information
    data = {
        "agency_name": agency_name,
        "address": address_full,
        "maps_link": maps_link,
        "Latitude": latitude,
        "Longitude": longitude
    }

    branch_data.append(data)
benin_data["benin"]=branch_data


# Save the data to a JSON file
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_benin.json', 'w') as file:
    json.dump(benin_data, file, indent=4)


