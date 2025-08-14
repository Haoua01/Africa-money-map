"""
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent



html_path = '/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bnda/bnda.html'

# Read the HTML file
with open(html_path, 'r') as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize an empty list to store the extracted data
location_data = []

# Loop through all geolocation-location divs
for location in soup.find_all('div', class_='geolocation-location js-hide'):
    # Extract name
    #print('in')
    #print(location)
    #name = location.find('div', class_='location-content').find('h2').get_text(strip=True)

    # Extract latitude and longitude
    latitude = location.find('meta', property='latitude')['content']
    longitude = location.find('meta', property='longitude')['content']
    
    # Store the extracted data in a dictionary
    location_dict = {
        "agence": "Agence BNDA",
        "Latitude": float(latitude),
        "Longitude": float(longitude)
    }
    
    # Append the dictionary to the list
    location_data.append(location_dict)


country_data={}
country_data["mali"]=location_data

# Save the data to a JSON file
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bnda/bnda.json', 'w') as f:
    json.dump(country_data, f, indent=4)
"""

import json
# Read the JSON file
with open('mali/bnda/bnda_corrected.json', 'r') as f:
    data = json.load(f)

mali_data = []
for branch in data["mali"]:
    mali_data.append({
        "bank": "bnda",
        "country": "mali",
        "address": branch["agence"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open('result/json_data_all/bnda.json', 'w', encoding='utf-8') as f:
    json.dump(mali_data, f, indent=4)

"""
import pandas as pd

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data['mali'])

# Save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/mali/bnda/bnda.shp')

"""