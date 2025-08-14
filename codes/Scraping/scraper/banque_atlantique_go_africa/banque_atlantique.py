import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
import re
import json
import pandas as pd
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


country_code={
    "togo": "https://www.goafricaonline.com/tg/28-banque-atlantique-lome-togo",
    "benin": "https://www.goafricaonline.com/bj/8905-banque-atlantique-cotonou-benin",
    "burkina": "https://www.goafricaonline.com/bf/15666-babf-banque-ouagadougou-burkina-faso",
    "mali": "https://www.goafricaonline.com/ml/134821-atlantique-banques-bamako-mali",
    "niger": "https://www.goafricaonline.com/ne/291485-bane-banque-atlantique-niger-niamey-niger",
    "senegal": "https://www.goafricaonline.com/sn/259286-atlantique-banques-dakar-senegal"
}


def remove_postal_address(address):
    # Expression régulière pour identifier les adresses de type "01 BP 522"
    postal_pattern_benin = r"\b\d{1,3}\sBP\s\d+\b|Lomé"
    postal_pattern_civ = r"\b\d{2}\sBP\s\d{3,4}\b|\bAbidjan\s\d{2}\b"
    postal=r"\b\d{1,3}\sBP\s\d+\b"

    
    # Remplacer les occurrences de l'adresse postale par une chaîne vide
    if country == "togo":
        cleaned_address = re.sub(postal_pattern_benin, "", address).strip()
    elif country == "cotedivoire":
        cleaned_address = re.sub(postal_pattern_civ, "", address).strip()
    else:
        cleaned_address = re.sub(postal, "", address).strip()
    
    return cleaned_address

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
        name_address = remove_postal_address(name_address)

        latitude, longitude = get_coordinates(name_address, api_key)

        # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
        agency_info = {
            'agence': name_address,
            'Latitude': latitude,
            'Longitude': longitude
        }

        # Ajouter l'agence à la liste
        agency_data.append(agency_info)
    country_data[country]=agency_data



# Sauvegarder les données dans un fichier JSON
with open('banque_atlantique_go_africa/banque_cleaned.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")

# correcting the json by filling the missing coordinates
with open('banque_atlantique_go_africa/banque_corrected.json', 'r') as f:
    data_all = json.load(f)

data = []
for country, country_info in data_all.items():
    for branch in country_info:
        data.append({
            "bank": "banque_atlantique",
            "country": country,
            "address": branch["agence"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 1
        })

df = pd.DataFrame(data)
print(df.head())

with open('result/json_data_all/banque_atlantique.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)


