
"""
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

# Raw HTML data (in your case, you may load this from a file or URL)
file = "/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/btci/IB.html"

with open(file, 'r', encoding='utf-8') as file:
    html_data = file.read()


# Parse the HTML content
soup = BeautifulSoup(html_data, 'html.parser')

# Find all geolocation-location elements
locations = soup.find_all('div', class_='geolocation-location')

# List to hold extracted data
location_data = []

# Loop through each location and extract relevant information
for location in locations:
    # Extract the name
    name = location.find('h2', class_='location-title').get_text(strip=True)
    
    # Extract the address
    address = location.find('div', class_='address-line').get_text(strip=True)
    
    # Extract the latitude and longitude from the meta tags
    latitude = float(location.find('meta', property='latitude')['content'])
    longitude = float(location.find('meta', property='longitude')['content'])
    
    # Append the data to the list
    location_data.append({
        "Name": name,
        "Address": address,
        "Latitude": latitude,
        "Longitude": longitude
    })

# Print the extracted data
for location in location_data:
    print(location)

# Optionally, save the data to a JSON file
import json
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/btci/btci_togo.json', 'w', encoding='utf-8') as json_file:
    json.dump(location_data, json_file, ensure_ascii=False, indent=4)
"""
import json

with open('btci/btci_togo.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

import pandas as pd
# Convert the JSON data to a DataFrame

data_branches = []
for branch in data:
    data_branches.append({
        "bank": "btci",
        "country": "togo",
        "address": branch["Address"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })
df = pd.DataFrame(data_branches)

with open('result/json_data_all/btci.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)



"""
#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/btci/btci.shp')
"""