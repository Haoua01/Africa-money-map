
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

"""
data_scraped=[['Agence centrale', 13.514983,2.108022, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20735224 <br> e-Mail : agencecentrale@sonibank.com', 3],['Agence Toumo', 13.504606,2.132618, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20341908 <br> e-Mail : agencetoumo@sonibank.com', 3],['Agence Liberté', 13.516353,2.114565, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20732073 <br> e-Mail : agenceliberté@sonibank.com', 3],['Agence Plateau', 0,0, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20724716 <br> e-Mail : agenceplateau@sonibank.com', 3],['Agence Harobanda', 13.491286,2.092567, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20735224 <br> e-Mail : agenceharobanda@sonibank.com', 3],['Agence Lazaret', 13.551639,2.112217, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20320135 <br> e-Mail : agencelazaret@sonibank.com', 3],['Agence Aéroport', 0,0, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20740001 <br> e-Mail : agenceaéroport@sonibank.com', 3],['Agence Koubia', 13.549717,2.060252, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20734740 <br> e-Mail : agencekoubia@sonibank.com', 3],['Agence Boulevard Tanimoune', 0,0, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20734740 <br> e-Mail : agenceroutefillingue@sonibank.com', 3],['Bureau Maourey', 0,0, 'Région : Niamey<br>Département. : Niamey<br>Tél. : 20732073 <br> e-Mail : bureaumaourey@sonibank.com', 3],['Agence Dosso', 13.045403,3.191258, 'Région : Dosso<br>Département. : Dosso<br>Tél. : 20650783 <br> e-Mail : agencedosso@sonibank.com', 3],['Agence Maradi', 13.804804,8.985246, 'Région : Maradi<br>Département. : Maradi<br>Tél. : 20410260 <br> e-Mail : agencemaradi@sonibank.com', 3],['Agence Zinder', 14.892012,5.237799, 'Région : Zinder<br>Département. : Zinder<br>Tél. : 20510049 <br> e-Mail : agencezinder@sonibank.com', 3],['Agence Tahoua', 16.970631,7.984384, 'Région : Tahoua<br>Département. : Tahoua<br>Tél. : 20610014 <br> e-Mail : agencetahoua@sonibank.com', 3],['Agence Agadez', 18.137814,7.384693, 'Région : Agadez<br>Département. : Agadez<br>Tél. : 20440826 <br> e-Mail : agenceagadez@sonibank.com', 3],['Agence Arlit', 18.737814,7.384693, 'Région : Agadez<br>Département. : Agadez<br>Tél. : 20452241 <br> e-Mail : agencearlit@sonibank.com', 3],['Agence Gaya', 11.893982,3.460308, 'Région : Dosso<br>Département. : Dosso<br>Tél. : 20680638 <br> e-Mail : bureaugaya@sonibank.com', 3],['Agence Konni', 13.801496,5.252671, 'Région : Tahoua<br>Département. : Tahoua<br>Tél. : 20640855 <br> e-Mail : bureaukonni@sonibank.com', 3],['Succursale Bénin', 6.354265,2.437627, 'Région : Bénin<br>Département. : Cotonou<br>Tél. : +229 21 31 89 <br> e-Mail : succursalebenin@sonibank.com', 3],]

#create a list of dictionaries from the list of lists
data_scraped_dicts = []
for data in data_scraped:
    data_scraped_dicts.append({'name':data[0],'Latitude':data[1],'Longitude':data[2]})

country_data={}
country_data['niger']=data_scraped_dicts

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/sonibank/sonibank.json', 'w') as outfile:
    json.dump(country_data, outfile)
"""
with open('niger/sonibank/sonibank-corrected.json', 'r') as f:
    data = json.load(f)

niger_data = []
for branch in data["niger"]:
    niger_data.append({
        "bank": "sonibank",
        "country": "niger",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open("result/json_data_all/sonibank_niger.json", "w", encoding='utf-8') as f:
    json.dump(niger_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd
df = pd.DataFrame(data['niger'])

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/niger/sonibank/sonibank-niger.shp')
"""


