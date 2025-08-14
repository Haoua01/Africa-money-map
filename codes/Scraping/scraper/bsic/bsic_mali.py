import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


# URL de la page à scraper (remplacez par l'URL réelle)
url = 'https://bsicbank.com/mali/reseaux/nos-agences/'

# Le pays de l'agence, à ajuster selon le pays spécifique
country = "Mali"

# Faire une requête GET pour obtenir la page HTML
response = requests.get(url)

# Parser la page avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver toutes les agences
agencies = soup.find_all('div', class_='bloc_pret')

# Initialiser une liste pour stocker les données des agences
agency_data = []

# Extraire les informations de chaque agence
for agency in agencies:
    # Trouver le nom de l'agence
    name = agency.find('h4').text.strip()
    
    # Trouver l'adresse jusqu'au saut de ligne
    address = agency.find('p').text.split('\n')[1].strip()

    #enlever le début de l'adresse jusqu'à ": "
    address = address.split(": ")[1]

    print(address)

    # Combiner "BSIC", le nom et l'adresse, puis ajouter le pays à la fin
    name_address = f"BSIC - {name} - {address} - {country}"
    
    # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
    agency_info = {
        'agence': name_address,
        'Latitude': '',
        'Longitude': ''
    }
    
    # Ajouter l'agence à la liste
    agency_data.append(agency_info)




# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/bsic/mali.json', 'w', encoding='utf-8') as json_file:
    json.dump(agency_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")





