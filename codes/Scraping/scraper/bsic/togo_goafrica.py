import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


# Le pays de l'agence, à ajuster selon le pays spécifique
country = ["Togo", ""]

country_code={
    "Togo": "https://www.goafricaonline.com/tg/1434-bsic-banques-lome-togo",
    "Cote d\'Ivoire": "https://www.goafricaonline.com/ci/53561-bsic-banques-abidjan-cote-ivoire"
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



        if country == "Togo":
            # Séparer le nom de l'agence et l'adresse
            name = name_address.split(":")[0].strip()
            address = name_address.split(":")[1].strip()

            # Ajouter le préfixe "BSIC" et le pays à la fin
            name_address_full = f"BSIC - {name} - {address}"
        elif country == "Cote d\'Ivoire":
            name_address_full = f"BSIC - {name_address}"

        # Créer un dictionnaire pour chaque agence avec latitude et longitude vides
        agency_info = {
            'agence': name_address_full,
            'Latitude': '',
            'Longitude': ''
        }

        # Ajouter l'agence à la liste
        agency_data.append(agency_info)
    country_data[country]=agency_data

# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/bsic/togo_civ_goafrica.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
