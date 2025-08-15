import json 
import os


data_cemac = {}
for country in ['benin','burkinafaso','ivorycoast', 'guineabissau', 'mali','niger','senegal','togo']:
    data_country = []
    with open(f'{country}.json', 'r') as f: #downloaded from citypopulation.de local storage
        data = json.load(f)
        for city in data['objs']:
            data_country.append({
                'Country': country,
                'City': city['name'],
                'Latitude': city['lat'],
                'Longitude': city['lng'],
                'Population': city['pop'][-1],
                'Area': city['area']
            })
    data_cemac[country] = data_country

with open('/workspaces/Africa-money-map/data/Regression/uemoa_communes.json', 'w') as f:
    json.dump(data_cemac, f)
        