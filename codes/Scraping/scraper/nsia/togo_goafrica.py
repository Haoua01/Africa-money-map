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




# Le pays de l'agence, à ajuster selon le pays spécifique
country = ["Togo", ""]

country_code={
    "Togo": "https://www.goafricaonline.com/tg/7810-nsia-benin-succursale-banques-lome-togo"
}

country_data={}
for country, url in country_code.items():
    # URL de la page à scraper (remplacez par l'URL réelle)
    url = url
    # Faire une requête GET pour obtenir la page HTML
    response = requests.get(url)

    # Parser la page avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les agences dans la liste (balise <li>)
    agencies = soup.find_all('li', class_='mb-6')

    # Initialiser une liste pour stocker les données des agences
    agency_data = []

    # Extraire les informations de chaque agence
    for agency in agencies:
        # Trouver le nom de l'agence et l'adresse dans les balises <address>
        address_tag = agency.find('address', class_='m-0 mb-2 text-gray-700')

            # Remplacer les <br> par " - " dans l'adresse
        for br_tag in address_tag.find_all('br'):
            br_tag.insert_before(' ')
            br_tag.insert_after(' ')
            br_tag.decompose()  # Remove <br> tag
        
        # Extraire le texte nettoyé
        name_address = address_tag.get_text(separator=' ', strip=True)



        # Séparer le nom de l'agence et l'adresse
        name = name_address.split(":")[0].strip()
        address = name_address.split(":")[1].strip()

        # Ajouter le préfixe "BSIC" et le pays à la fin
        name_address_full = f"NSIA - {name} - {address}"

        latitude, longitude = get_coordinates(name_address_full, api_key)


        # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
        agency_info = {
            'agence': name_address_full,
            'Latitude': latitude,
            'Longitude': longitude
        }

        # Ajouter l'agence à la liste
        agency_data.append(agency_info)
    country_data[country]=agency_data

# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/togo_goafrica.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
