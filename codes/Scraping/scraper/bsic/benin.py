import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

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



# URL de la page à scraper (remplacez par l'URL réelle)
url = 'https://bsicbank.com/benin/category/notre-reseau/nos-agences/'  # Replace with actual URL

# Le pays de l'agence, à ajuster selon le pays spécifique
country = "Benin"

# Faire une requête GET pour obtenir la page HTML
response = requests.get(url)

# Parser la page avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver toutes les agences
agencies = soup.find_all('article', class_='cmsmasters-blog__post')

# Initialiser une liste pour stocker les données des agences
agency_data = []

# Extraire les informations de chaque agence
for agency in agencies:
    # Trouver le nom de l'agence
    name = agency.find('h3', class_='entry-title').text.strip()

    # Trouver l'adresse et le téléphone dans le paragraphe
    address_paragraph = agency.find('div', class_='entry-content').find('p').text.strip()
    address = address_paragraph.split("Adresse :")[1].split("Téléphone :")[0].strip()
    name_address = f"{address}, Cotonou, {country}"
    lat, lng = get_coordinates(name_address, api_key)



    # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
    agency_info = {
        'bank': 'bsic',
        'country': "benin",
        'address': address[:80],
        'Latitude': lat,
        'Longitude': lng,
        'geocoded':1
    }
    
    # Ajouter l'agence à la liste
    agency_data.append(agency_info)

# Sauvegarder les données dans un fichier JSON
with open('/workspaces/Africa-money-map/codes/Scraping/scraper/bsic/benin.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(agency_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
