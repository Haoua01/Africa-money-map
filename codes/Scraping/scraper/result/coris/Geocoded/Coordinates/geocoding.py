import requests
import json
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

"""
# Charger votre fichier JSON (assurez-vous de mettre le bon chemin de fichier)
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/coris/coris_corrected.json', 'r') as file:
    data = json.load(file)

# Liste des pays
countries = ["senegal", "cotedivoire", "togo", "benin"]

# Parcourir chaque pays et chaque branche
for country in countries:
    for entry in data[country]:
        # Combiner "Coris Bank", "name", "address" et le pays dans l'attribut "branch"
        entry["branch"] = f"Coris Bank - {entry['name']} - {entry['address']}, {country.capitalize()}"

        # Vous pouvez également supprimer les attributs "name" et "address" si vous n'en avez plus besoin
        del entry["name"]
        del entry["address"]

# Sauvegarder le fichier mis à jour avec la nouvelle structure
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/coris/Geocoded/Coordinates/coris_corrected_geocoding.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Les branches ont été mises à jour avec succès.")

"""


with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/coris/Geocoded/Coordinates/coris_corrected_geocoding.json', 'r') as file:
    data = json.load(file)

# Liste des pays
countries = ["senegal", "cotedivoire", "togo", "benin"]


# Fonction pour remplir les coordonnées manquantes
def fill_coordinates(country_data):
    for entry in country_data:
        if not entry.get("Latitude") or not entry.get("Longitude"):  # Vérifie si les coordonnées manquent
            #print(f"Récupération des coordonnées pour : {entry['address']}")
            latitude, longitude = get_coordinates(entry['branch'], api_key)
            
            # Si les coordonnées sont obtenues, les ajouter au JSON
            if latitude and longitude:
                entry["Latitude"] = latitude
                entry["Longitude"] = longitude


for country in countries:
    print(f"Mise à jour des coordonnées pour le pays : {country}")
    fill_coordinates(data[country])

countries_with_coordinates=["burkina", "mali", "niger"]
for country in countries_with_coordinates:
    for entry in data[country]:
        # Convert Latitude and Longitude to float
        entry["lat"] = float(entry["lat"]) if entry["lat"] else None
        entry["lng"] = float(entry["lng"]) if entry["lng"] else None
            

# Sauvegarder le fichier mis à jour
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/coris/Geocoded/Coordinates/coris_geocoding_float.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Les coordonnées manquantes ont été mises à jour.")


