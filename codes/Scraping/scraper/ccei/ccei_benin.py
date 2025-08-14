"""
from bs4 import BeautifulSoup
import json
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent


url="https://www.bangebj.com/index.php/fr/"

# Raw HTML extract (new HTML structure)
html_data = '''
<div id="sppb-addon-osm-1570727077440" class="sppb-addon-openstreetmap " data-location='[{"address":"Agence Pricipale GANHI","latitude":"6.35409","longitude":" 2.4381","custom_icon":""},{"address":"Agence MISSEBO","latitude":"6.36231","longitude":" 2.43697","custom_icon":""},{"address":"Agence PARAKOU","latitude":"9.3388","longitude":"2.6287","custom_icon":""},{"address":"Manhattan Island","latitude":"40.7970","longitude":"-73.9491","custom_icon":""}]' data-mapstyle="OpenStreetMap.Mapnik" data-mapzoom="15" data-mousescroll="0" data-dragging="0" data-zoomcontrol="1" data-attribution="1"></div>
'''

# Parse the HTML
soup = BeautifulSoup(html_data, 'html.parser')

# Extract the data-location attribute (the JSON string)
data_str = soup.find('div', {'id': 'sppb-addon-osm-1570727077440'}).get('data-location')

# Parse the JSON string into a Python list
locations = json.loads(data_str)

# Prepare a dictionary for saving the extracted data
country_data = {}
branch_data = []

# Extract relevant data from the JSON list
for location in locations:
    address = location.get('address')
    latitude = float(location.get('latitude'))
    longitude = float(location.get('longitude'))
    
    branch_data.append({
        "Address": address,
        "Latitude": latitude,
        "Longitude": longitude
    })

# Save the data to a dictionary
country_data["benin"] = branch_data



# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/ccei/ccei_benin.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
"""
import json
import pandas as pd
with open('ccei/ccei_benin_corrected.json', 'r') as f:
    data_all = json.load(f)

data_benin = []
for country, country_info in data_all.items():
    for branch in country_info:
        data_benin.append({
            "bank": "bange",
            "country": country,
            "address": branch["Address"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 0
        })

with open('result/json_data_all/bange.json', 'w', encoding='utf-8') as f:
    json.dump(data_benin, f, ensure_ascii=False, indent=4)
"""
df = pd.DataFrame(data_all["benin"])
#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/ccei/ccei.shp')





"""