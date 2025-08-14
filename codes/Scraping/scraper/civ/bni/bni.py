import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent
"""
import pandas as pd

import geopandas as gpd
from shapely.geometry import Point

# Your JSON data (the implantationsList)
implantationsList = [{"uid":25,"adr1":"En face du Grand March\u00e9, mitoyen au TRESOR","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 35 90 00 92 \/ 94 \/ 95","name":"ABENGOUROU","type_map":"3","actif":"1","coordX":"-3.487329","coordY":"6.730453"},{"uid":24,"adr1":"Face \u00e0 l'H\u00f4pital G\u00e9n\u00e9ral d'Abobo-Sud, \u00e0 proximit\u00e9 du Grand- March\u00e9 <br>01 BP 670 Abidjan 01","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 25 23 00 54 19 \/ 26","name":"ABOBO","type_map":"3","actif":"1","coordX":"-4.015669","coordY":"5.423586"},{"uid":4,"adr1":"A proximit\u00e9 de l'H\u00f4pital G\u00e9n\u00e9ral d'Adjam\u00e9 <br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00(225) 27 20 30 51 65 \/ 66","name":"ADJAME BANFORA","type_map":"3","actif":"1","coordX":"-4.024789","coordY":"5.348504"},{"uid":37,"adr1":"Carrefour March\u00e9 Gouro","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 31 99 00","name":"ADJAME ST-MICHEL","type_map":"3","actif":"1","coordX":"-4.023106","coordY":"5.348980"},{"uid":64,"adr1":"Quartier Plateau \u00e0 c\u00f4t\u00e9 de l'\u00c9glise Catholique Notre Dame d'Anyama.","horaire":"<i>Agence,Guichet<\/i><br>","tel":"2786850040","name":"ANYAMA","type_map":"3","actif":"1","coordX":"-4.051922","coordY":"5.500326"},{"uid":63,"adr1":"Angr\u00e9 Bessikoi - A proximit\u00e9 du nouveau CHU","horaire":"<i>Agence,Guichet<\/i><br>","tel":"2720277107","name":"COCOCY ANGRE CHU","type_map":"3","actif":"1","coordX":"-3.956594","coordY":"5.398677"},{"uid":47,"adr1":"Axe principale menant au rond-point \u00ab ADO \u00bb ; \u00e0 proximit\u00e9 de cash Djibi","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 30 35 19","name":"COCODY 9\u00e8me TRANCHE","type_map":"3","actif":"1","coordX":"-3.973258","coordY":"5.383731"},{"uid":32,"adr1":"Face au th\u00e9\u00e2tre de la cit\u00e9 et la Cit\u00e9 universitaire \"Cit\u00e9 Rouge\" <br>01 BP 670 Abidjan 01","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 22 48 27 10 \/ 11","name":"COCODY DANGA","type_map":"3","actif":"1","coordX":"-4.005023","coordY":"5.33774"},{"uid":15,"adr1":"Axe Boulevard Latrille - Route d'Agban <br>01 BP 670 Abidjan 01","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 22 40 56 85 \/ 86","name":"COCODY II PLATEAUX AGBAN","type_map":"3","actif":"1","coordX":"-4.000335","coordY":"5.368401"},{"uid":23,"adr1":"Boulevard Latrille - Carrefour Duncan <br>01 BP 670 Abidjan 01","horaire":"<i>Guichet,Agence,Point digital<\/i><br>","tel":"00 (225) 27 22 52 95 60 \/ 61 \/ 62","name":"COCODY II PLATEAUX LATRILLE","type_map":"3","actif":"1","coordX":"-3.997371","coordY":"5.377640"},{"uid":55,"adr1":"Cocody Riviera 4 <br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"Bient\u00f4t disponible","name":"COCODY RIVIERA M'POUTO","type_map":"3","actif":"1","coordX":"-3.948175","coordY":"5.328371"},{"uid":14,"adr1":"Axe principal Palmeraie-Rosiers <br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 22 49 01 50 \/ 51 \/ 52","name":"COCODY RIVIERA PALMERAIE","type_map":"3","actif":"1","coordX":"-3.958836","coordY":"5.369861"},{"uid":45,"adr1":"A proximit\u00e9 de la Mairie de Koumassi","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 30 30 84 \/ 85","name":"KOUMASSI MAIRIE","type_map":"3","actif":"1","coordX":"-3.969805","coordY":"5.290571"},{"uid":13,"adr1":"Rue Pierre et Marie Curie <br>Angle de la rue du Dr Blanchard, face \u00e0 Nice Cream <br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 21 75 82 85 \/ 86 \/ 87","name":"MARCORY ZONE 4","type_map":"3","actif":"1","coordX":"-3.982505","coordY":"5.291463"},{"uid":38,"adr1":"Avenue Terrason de Foug\u00e8res 2\u00e8me \u00e9tage de l'immeuble ALLIANCE, <br> Face c\u00f4t\u00e9 entr\u00e9e salle des f\u00eates de l'immeuble de la CAISTAB <br> 01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 30 30 22 \/ 11","name":"PLATEAU ALLIANCE","type_map":"3","actif":"1","coordX":"-4.017922","coordY":"5.325895"},{"uid":30,"adr1":"Place de la R\u00e9publique<br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 21 75 82 85 \/ 86 \/ 87","name":"PLATEAU REPUBLIQUE","type_map":"3","actif":"1","coordX":"-4.019727","coordY":"5.318434"},{"uid":46,"adr1":"Axe principale Riviera Palmeraie - Bingerville - Carrefour dit \u00ab Faya \u00bb sur la droite, en face du Mall Playce","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 20 30 30 24","name":"RIVIERA ABATTA","type_map":"3","actif":"1","coordX":"-3.979014","coordY":"5.345541"},{"uid":3,"adr1":"Treichville Grand March\u00e9 Avenue Victor Biaka pr\u00e8s de la Maison du parti PDCI","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 21 75 55 35 \/ 32","name":"TREICHVILLE MARCH\u00c9","type_map":"3","actif":"1","coordX":"-4.014052","coordY":"5.309464"},{"uid":12,"adr1":"Axe principal - Entre les carrefours Figayo et Keneya <br>01 BP 670 Abidjan 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 30 35 31","name":"YOPOUGON KENEYA","type_map":"3","actif":"1","coordX":"-4.073131","coordY":"5.347487"},{"uid":36,"adr1":"Axe Station Lubafrique - Eglise Ste Rita de Niangon","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 23 46 94 80","name":"YOPOUGON MAROC","type_map":"3","actif":"1","coordX":"-4.103809","coordY":"5.330211"},{"uid":22,"adr1":"Site PALM-CI de Ehania","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 21 30 48 50","name":"ABOISSO EHANIA","type_map":"3","actif":"1","coordX":"-3.053246","coordY":"5.285542"},{"uid":65,"adr1":"Voie Principale non loin de la Sous Pr\u00e9fecture","horaire":"<i>Agence,Guichet<\/i><br>","tel":"27 20 30 30 30","name":"AGENCE BNI","type_map":"3","actif":"1","coordX":"17.7636824,6","coordY":"6.571017"},{"uid":11,"adr1":"Voie principale Abidjan - Aboisso <br>01 BP 670 Abidjan 01","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 21 30 97 70 \/ 71 \/ 72","name":"BONOUA","type_map":"3","actif":"1","coordX":"-3.597406","coordY":"5.268620"},{"uid":34,"adr1":"Rue Bernard Dadi\u00e9, Quartier Commerce <br>01 BP 1363 Bouak\u00e9 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 31 65 67 45 \/ 49","name":"BOUAKE COMMERCE","type_map":"3","actif":"1","coordX":"-5.028895","coordY":"7.682638"},{"uid":16,"adr1":"March\u00e9 de Gros de Bouak\u00e9 <br> 01 BP 1363 Bouak\u00e9 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 31 65 67 67 \/ 68 \/ 69","name":"BOUAKE MARCHE DE GROS","type_map":"3","actif":"1","coordX":"-5.022602","coordY":"7.697940"},{"uid":18,"adr1":"Carrefour des Axes Tengr\u00e9la - Odienne, <br>apr\u00e8s la Station Total, \u00e0 proximit\u00e9 de l'ancien Commissariat","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 36 86 57 90 \/ 91 \/ 92","name":"BOUNDIALI","type_map":"3","actif":"1","coordX":"-6.484987","coordY":"9.522925"},{"uid":26,"adr1":"Quartier Soleil, Route de Du\u00e9kou\u00e9","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 32 76 73 40 \/ 41 \/42","name":"DALOA","type_map":"3","actif":"1","coordX":"-6,4594770","coordY":"6,8845990"},{"uid":19,"adr1":"Carrefour de Korhogo, en face du March\u00e9","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 36 86 90 62 \/ 65","name":"FERKESSEDOUGOU","type_map":"3","actif":"1","coordX":"-5.197731","coordY":"9.592457"},{"uid":27,"adr1":"Quartier Commerce, entre l'H\u00f4tel de ville et le march\u00e9","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 32 77 71 95 \/ 96 \/ 97","name":"GAGNOA","type_map":"3","actif":"1","coordX":"-5,9458390","coordY":"6,1306740"},{"uid":39,"adr1":"Axe Grand-Lahou Site PALMCI Irobo","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 20 20 99 74 \/ 76","name":"GRAND-LAHOU IROBO","type_map":"3","actif":"1","coordX":"-4,7958980","coordY":"5,2973700"},{"uid":35,"adr1":"Rue des Banques","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 36 85 00 40 \/ 41 \/45","name":"KORHOGO","type_map":"3","actif":"1","coordX":"-5.631852","coordY":"9.457337"},{"uid":28,"adr1":"Village de Tongon, Mine d'or Rangold \u00e0 65 km de Korhogo","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 07 48 59 05 32","name":"KORHOGO TONGON","type_map":"3","actif":"1","coordX":"-5.730662","coordY":"9.901097"},{"uid":40,"adr1":"Quartier Commerce - Route de Facobly \/ Lac","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 33 79 18 20","name":"MAN","type_map":"3","actif":"1","coordX":"-7.545198","coordY":"7.412676"},{"uid":20,"adr1":"Axe San Pedro - Soubr\u00e9, \u00e0 proximit\u00e9 de la gare routi\u00e8re","horaire":"<i>Guichet,Agence<\/i><br>","tel":"00 (225) 27 34 72 66 15 \/ 16 \/ 17","name":"MEAGUI","type_map":"3","actif":"1","coordX":"-6.558391","coordY":"5.410757"},{"uid":10,"adr1":"Rue des banques <br> 01 BP 95 SAN PEDRO 01","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 34 71 92 00 \/ 01 \/ 02","name":"SAN-PEDRO CITE","type_map":"3","actif":"1","coordX":"-6,6347400","coordY":"4,7477510"},{"uid":42,"adr1":"Site PALMCI Iboke V2","horaire":"<i>Agence,Guichet<\/i><br>","tel":"00 (225) 27 20 20 99 77","name":"SAN-PEDRO IBOKE","type_map":"3","actif":"1","coordX":"-7,4071810","coordY":"4,6823450"},{"uid":7,"adr1":"Axe principal Abidjan-Bouak\u00e9, Quartier habitat <br>BP 1531 Yamoussoukro","horaire":"<i>Point digital,Agence,Guichet<\/i><br>","tel":"00 (225) 27 30 64 09 54 \/ 55","name":"YAMOUSSOUKRO","type_map":"3","actif":"1","coordX":"-5.279204","coordY":"6.821579"}];

country_data={}
# Extracting Latitude and Longitude for each agency
coordinates = []

for agency in implantationsList:
    name = agency['name']
    coord_x = agency['coordX']
    coord_y = agency['coordY']
    coordinates.append({'name': name, 'Latitude': coord_y, 'Longitude': coord_x})

# Printing out the results
for coord in coordinates:
    print(f"Agency: {coord['name']}, Latitude: {coord['Latitude']}, Longitude: {coord['Longitude']}")

country_data['cotedivoire'] = coordinates

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bni/bni.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, indent=4)
"""
with open('civ/bni/bni_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

civ_data = []
for agency in data['cotedivoire']:
    civ_data.append({
        "bank": 'bni',
        "country": 'civ',
        "address": agency['name'],
        "Latitude": float(agency['Latitude']),
        "Longitude": float(agency['Longitude']),
        "geocoded": 0
    })

with open('result/json_data_all/bni.json', 'w', encoding='utf-8') as f:
    json.dump(civ_data, f, indent=4)


"""
df = pd.DataFrame(data['cotedivoire'])


geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/bni/bni.shp')"""