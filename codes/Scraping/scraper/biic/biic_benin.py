"""
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

url="https://www.biic-bank.com/fr/contact-particulier.html"

# Raw HTML extract
html_data = '''
<div class="uk-position-relative uk-position-z-index uk-dark uk-margin" style="min-height: 80vh;" uk-map data-map-type="leaflet">
    <script type="application/json">
    {"markers":[{"lat":6.3702118,"lng":2.4110004,"title":"BIIC GOHO","show_popup":true},
                {"lat":6.4990718,"lng":2.6253361,"title":"BIIC KOKOYE","show_popup":true},
                {"lat":6.38601285,"lng":2.3801041527084132,"title":"BIIC STADE DE L'AMITIÉ","show_popup":true},
                {"lat":6.3714675,"lng":2.409769257120141,"title":"BIIC ETOILE","show_popup":true},
                {"lat":6.3633476,"lng":2.4249277,"title":"BIIC MARO MILITAIRE","show_popup":true},
                {"lat":6.3755322,"lng":2.4314042,"title":"BIIC DANTOKPA","show_popup":true},
                {"lat":6.3724293,"lng":2.4262832,"title":"BIIC JÉRICHO","show_popup":true},
                {"lat":6.3705625,"lng":2.4166009,"title":"BIIC MARINA","show_popup":true},
                {"lat":8.16811735,"lng":2.2291357527306785,"title":"BIIC GLAZOUÉ","show_popup":true},
                {"lat":7.9852170000000005,"lng":2.5417577150572566,"title":"BIIC SAVÉ","show_popup":true},
                {"lat":9.3400159,"lng":2.6278258,"title":"BIIC PARAKOU","show_popup":true},
                {"lat":10.25395885,"lng":2.750742720088743,"title":"BIIC BEMBEREKE","show_popup":true},
                {"lat":11.32625415,"lng":2.473040680223342,"title":"BIIC BANIKOARA","show_popup":true},
                {"lat":11.2849785,"lng":3.046420881638551,"title":"BIIC KANDI","show_popup":true},
                {"lat":11.8618128,"lng":3.3862982,"title":"BIIC MALANVILLE","show_popup":true}],
     "clustering":true,"controls":true,"dragging":false,"max_zoom":18,"min_zoom":0,
     "poi":false,"type":"roadmap","zoom":"5","zooming":true,"center":{"lat":6.3702118,"lng":2.4110004},
     "lazyload":true,"library":"leaflet","baseUrl":"\/templates\/yootheme\/vendor\/assets\/leaflet\/leaflet\/dist",
     "clusterBaseUrl":"~assets\/leaflet\/markercluster\/dist"}
    </script>
</div>
'''

# Parse the HTML
soup = BeautifulSoup(html_data, 'html.parser')

# Extract the JSON content from the <script> tag
json_str = soup.find('script', {'type': 'application/json'}).string

# Parse the JSON string into a Python dictionary
data = json.loads(json_str)

# Print the extracted data
print(json.dumps(data, indent=4))

#extract "lat", "lng", "title" from the markers
markers = data.get('markers', [])
country_data={}
branch_data = []
for marker in markers:
    Title = marker.get('title')
    Latitude = marker.get('lat')
    Longitude = marker.get('lng')
    #write a json
    branch_data.append({
        "Title": Title,
        "Latitude": Latitude,
        "Longitude": Longitude
    })
country_data["benin"]=branch_data

# Sauvegarder les données dans un fichier JSON
with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/biic/biic_benin.json', 'w', encoding='utf-8') as json_file:  # Update with actual path
    json.dump(country_data, json_file, ensure_ascii=False, indent=4)

print("Données sauvegardées")
"""
import json
import pandas as pd
with open('biic/biic_benin.json', 'r') as f:
    data_all = json.load(f)


df = pd.DataFrame(data_all)

data_benin = []
for country, country_info in data_all.items():
    for branch in country_info:
        data_benin.append({
            "bank": "biic",
            "country": country,
            "address": branch["Title"][:80],
            "Latitude": branch["Latitude"],
            "Longitude": branch["Longitude"],
            "geocoded": 0
        })

df_benin = pd.DataFrame(data_benin)
with open('result/json_data_all/biic.json', 'w', encoding='utf-8') as f:
    json.dump(df_benin.to_dict(orient='records'), f, ensure_ascii=False, indent=4)
    
"""
#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/biic/biic.shp')




"""
