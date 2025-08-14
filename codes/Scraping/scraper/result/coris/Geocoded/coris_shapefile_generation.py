"""
import pandas as pd
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/Coordinates/coris_geocoding_float.json', 'r') as f:
    country_data = json.load(f)

data=[]

countries_with_coordinates=["burkina", "mali", "niger", "guineebissau"]

countries_geocoded=["senegal", "benin", "togo", "cotedivoire"]

for country, country_info in country_data.items():
    if country in countries_with_coordinates:
        for branch in country_info:
            data.append({
                'label': "scrapped",
                'Latitude': branch['lat'],
                'Longitude': branch['lng']
            })
    elif country in countries_geocoded:
        for branch in country_info:
            data.append({
                'label': "geocoded",
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude']
            })


df = pd.DataFrame(data)

print(df)

#save geolocations to a shapefile and keep label
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]

import pandas as pd
import json

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/Coordinates/coris_geocoding_float.json', 'r') as f:
    country_data = json.load(f)

data=[]

countries_with_coordinates=["burkina", "mali", "niger", "guineebissau"]

countries_geocoded=["senegal", "benin", "togo", "cotedivoire"]

for country, country_info in country_data.items():
    if country in countries_with_coordinates:
        for branch in country_info:
            data.append({
                'label': "scrapped",
                'Latitude': branch['lat'],
                'Longitude': branch['lng']
            })
    elif country in countries_geocoded:
        for branch in country_info:
            data.append({
                'label': "geocoded",
                'Latitude': branch['Latitude'],
                'Longitude': branch['Longitude']
            })


df = pd.DataFrame(data)

print(df)

#save geolocations to a shapefile and keep label
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]

"""
import pandas as pd
import json

with open('result/coris/Geocoded/Coordinates/coris_geocoding_float.json', 'r', encoding='utf-8') as f:
    country_data = json.load(f)

data=[]

countries_with_coordinates=["burkina", "mali", "niger", "guinee"]

countries_geocoded=["senegal", "benin", "togo", "cotedivoire"]

for country, country_info in country_data.items():
    if country in countries_with_coordinates:
        for branch in country_info:
            data.append({
                'bank': "coris", 
                'country': country,
                'address': (branch['address'][:50] + ' - ' + branch['city'] + ", " + branch['country'])[:80],  
                'Latitude': branch['lat'],
                'Longitude': branch['lng'],
                'geocoded': 0
            })
    elif country in countries_geocoded:
        if country == "cotedivoire":
            for branch in country_info:
                data.append({
                    'bank': "coris",
                    'country': "civ",
                    'address': branch['branch'][:80],
                    'Latitude': branch['Latitude'],
                    'Longitude': branch['Longitude'],
                    'geocoded': 1
                })
        else:
            for branch in country_info:
                data.append({
                    'bank': "coris",
                    'country': country,
                    'address': branch["branch"][:80],
                    'Latitude': branch['Latitude'],
                    'Longitude': branch['Longitude'],
                    'geocoded': 1
                })
        


df = pd.DataFrame(data)

with open('result/json_data_all/coris.json', 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)


print(df)
"""
#save geolocations to a shapefile and keep label
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]

gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/coris/Geocoded/Coordinates/coris_geocoded.shp")





"""