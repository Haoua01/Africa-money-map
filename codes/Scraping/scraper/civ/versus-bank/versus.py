
"""import urllib.parse
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

# The URL-encoded string (you should paste your entire string here)
url_encoded_data = "%7B%22categoriesEnabled%22%3Atrue%2C%22categories%22%3A%5B%5D%2C%22icons%22%3A%5B%7B%22value%22%3A%22%22%2C%22name%22%3A%22%20-%20None%20-%20%22%2C%22visible%22%3Afalse%7D%2C%7B%22value%22%3A%2271d838d7-e8a4-4772-b21f-dc34e7404a12%22%2C%22name%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F09%5C%2Fmarker.png%22%2C%22preview%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F09%5C%2Fmarker.png%22%2C%22iconType%22%3A%22custom%22%2C%22iconLibrary%22%3A%22number9%22%2C%22iconCustom%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F09%5C%2Fmarker.png%22%2C%22iconColor%22%3A%22%22%2C%22iconSize%22%3A40%7D%5D%2C%22lang%22%3A%22fr%22%2C%22distanceUnits%22%3A%22km%22%2C%22markers%22%3A%5B%7B%22position%22%3A%22Angle%20Boulevard%20Botreau%20Roussel%20-%20Rue%20Priv%5Cu00e9e%20CRRAE-UMOA%20%28Plateau%2001%20BP%202056%20Abidjan%2001%22%2C%22coordinates%22%3A%225.320978999999999%2C%20-4.0150969%22%2C%22icon%22%3A%22%22%2C%22iconUrl%22%3A%22%22%2C%22infoWindow%22%3Atrue%2C%22infoTitle%22%3A%22AGENCE%20PLATEAU%22%2C%22infoDescription%22%3A%22%22%2C%22infoImage%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F09%5C%2Fversus-siege-scaled.jpg%22%2C%22infoAddress%22%3A%22SI%5Cu00c8GE%20et%20Agence%20principale%20Immeuble%20CRRAE-UEMOA%20Angle%20Botreau%20Roussel%20%5C%2F%20Avenue%20Joseph%20ANOMA%22%2C%22infoSite%22%3A%22http%3A%5C%2F%5C%2Fwww.versusbank.ci%22%2C%22infoPhone%22%3A%22%28%2B225%29%2020%2025%2060%2060%20-%2020%2025%2060%2090%20Fax%20%3A%20%28%2B225%29%2020%2025%2060%2099%22%2C%22infoEmail%22%3A%22standard%40versusbank.com%22%2C%22infoWorkingHours%22%3A%22Du%20lundi%20au%20Vendredi%20%3A%208H%20-15H%20%5C%2F%20Samedi%20%3A%20Ferm%5Cu00e9e%20%5Cu00e0%20la%20client%5Cu00e8le%20%5C%2F%20n%27ouvre%20pas%20les%20samedis%22%2C%22infoWindowOpenedByDefault%22%3Atrue%2C%22markerClickAction%22%3A%22infoWindow%22%2C%22animation%22%3A%22none%22%2C%22linkUrl%22%3A%22%22%2C%22category%22%3A%22%22%7D%2C%7B%22position%22%3A%229255%2B2R%20Abidjan%22%2C%22coordinates%22%3A%225.357562499999999%2C%20-3.9904375%22%2C%22icon%22%3A%2271d838d7-e8a4-4772-b21f-dc34e7404a12%22%2C%22iconUrl%22%3A%22%22%2C%22infoWindow%22%3Atrue%2C%22infoTitle%22%3A%22AGENCE%20II%20PLATEAUX%22%2C%22infoDescription%22%3A%22%22%2C%22infoImage%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F10%5C%2Fversus-bank-2-plateaux-map.jpg%22%2C%22infoAddress%22%3A%22Cocody%20-%20II%20Plateaux%2C%20Rue%20des%20Jardins%22%2C%22infoSite%22%3A%22http%3A%5C%2F%5C%2Fwww.versusbank.ci%22%2C%22infoPhone%22%3A%22%28%2B225%29%2020%2025%2062%2019%20-%2020%2025%2062%2020%20Fax%20%3A%20%28%2B225%29%2022%2041%2055%2013%22%2C%22infoEmail%22%3A%22standard%40versusbank.com%22%2C%22infoWorkingHours%22%3A%22Lundi%20-%20Vendredi%20%20De%208h%20%5Cu00e0%2017h%22%2C%22infoWindowOpenedByDefault%22%3Atrue%2C%22markerClickAction%22%3A%22infoWindow%22%2C%22animation%22%3A%22none%22%2C%22linkUrl%22%3A%22%22%2C%22category%22%3A%22%22%2C%22id%22%3A%221e924477-b0b7-416f-875e-a8cd83cc4dd1%22%7D%2C%7B%22position%22%3A%2272Q9%2BJ2%20Abidjan%22%2C%22coordinates%22%3A%225.2890625%2C%20-3.9824375%22%2C%22icon%22%3A%2271d838d7-e8a4-4772-b21f-dc34e7404a12%22%2C%22iconUrl%22%3A%22%22%2C%22infoWindow%22%3Atrue%2C%22infoTitle%22%3A%22AGENCE%20ZONE%204%20C%22%2C%22infoDescription%22%3A%22%22%2C%22infoImage%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2020%5C%2F09%5C%2Fagence-zone-4.jpg%22%2C%22infoAddress%22%3A%22Rue%20Pierre%20%26%20Marie%20Curie%22%2C%22infoSite%22%3A%22http%3A%5C%2F%5C%2Fwww.versusbank.ci%22%2C%22infoPhone%22%3A%22%28%2B225%29%2020%2025%2062%2031%20-%2020%2025%2062%2032%20Fax%20%3A%20%28%2B225%29%2021%2024%2006%2010%22%2C%22infoEmail%22%3A%22standard%40versusbank.com%22%2C%22infoWorkingHours%22%3A%22Lundi%20-%20Vendredi%20%20De%208h%20%5Cu00e0%2017h%22%2C%22infoWindowOpenedByDefault%22%3Atrue%2C%22markerClickAction%22%3A%22infoWindow%22%2C%22animation%22%3A%22none%22%2C%22linkUrl%22%3A%22%22%2C%22category%22%3A%22%22%2C%22id%22%3A%227bf507f8-c9a5-4778-b2be-9ad207251df8%22%7D%2C%7B%22position%22%3A%22abatta%22%2C%22coordinates%22%3A%225.3259656%2C%20-3.9158216%22%2C%22icon%22%3A%2271d838d7-e8a4-4772-b21f-dc34e7404a12%22%2C%22iconUrl%22%3A%22%22%2C%22infoWindow%22%3Atrue%2C%22infoTitle%22%3A%22Agence%20d%27ABATTA%22%2C%22infoDescription%22%3A%22%22%2C%22infoImage%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2021%5C%2F03%5C%2FSiege-Abata.jpg%22%2C%22infoAddress%22%3A%22abatta%22%2C%22infoSite%22%3A%22https%3A%5C%2F%5C%2Fwww.versusbank.ci%22%2C%22infoPhone%22%3A%22%2B225%2027%2020%2025%2060%2060%22%2C%22infoEmail%22%3A%22standard%40versusbank.com%22%2C%22infoWorkingHours%22%3A%22Lundi%20-%20Vendredi%20%20De%208h%20%5Cu00e0%2017h%22%2C%22infoWindowOpenedByDefault%22%3Atrue%2C%22markerClickAction%22%3A%22infoWindow%22%2C%22animation%22%3A%22none%22%2C%22linkUrl%22%3A%22%22%2C%22category%22%3A%22%22%2C%22id%22%3A%226b226bc4-d5fd-4f15-b242-5f00f6c4120c%22%7D%2C%7B%22position%22%3A%22Cocody%20Angr%5Cu00e9%20face%20CHU%20d%27Angr%5Cu00e9%22%2C%22coordinates%22%3A%225.4011252%2C%20-3.9575344%22%2C%22infoTitle%22%3A%22AGENCE%20ANGRE%20CHU%22%2C%22category%22%3A%22%22%2C%22icon%22%3A%2271d838d7-e8a4-4772-b21f-dc34e7404a12%22%2C%22infoDescription%22%3A%22%22%2C%22infoImage%22%3A%22https%3A%5C%2F%5C%2Fversusbank.ci%5C%2Fwp-content%5C%2Fuploads%5C%2F2023%5C%2F01%5C%2Fversus-chu-angre.jpg%22%2C%22infoAddress%22%3A%22Cocody%20Angr%5Cu00e9%20face%20CHU%20d%27Angr%5Cu00e9%22%2C%22infoSite%22%3A%22http%3A%5C%2F%5C%2Fwww.versusbank.ci%22%2C%22infoPhone%22%3A%22%28%2B225%29%2027%2020%2025%2062%2031%22%2C%22infoEmail%22%3A%22standard%40versusbank.com%22%2C%22infoWorkingHours%22%3A%22Lundi-Vendredi%20de%209h%20%5Cu00e0%2017h%20Samedi%20de%209h30%20%5Cu00e0%2012h30%22%2C%22markerClickAction%22%3A%22infoWindow%22%2C%22infoWindowOpenedByDefault%22%3Atrue%2C%22linkUrl%22%3A%22%22%2C%22animation%22%3A%22none%22%7D%5D%2C%22mapType%22%3A%22roadmap%22%2C%22center%22%3A%22auto%22%2C%22zoom%22%3A%2217%22%2C%22controls%22%3A%5B%22zoom%22%2C%22mapType%22%2C%22scale%22%2C%22streetView%22%2C%22rotate%22%2C%22fullScreen%22%5D%2C%22markerClusterEnabled%22%3Atrue%2C%22markerClusterZoom%22%3Atrue%2C%22markerClusterMin%22%3A2%2C%22markerClusterIcon%22%3A%22default%22%2C%22markerClusterIconColor%22%3A%22rgb%28219%2C%2095%2C%200%29%22%2C%22markerClusterIconUrl%22%3Anull%2C%22markerClusterSize%22%3A52%2C%22infoDirections%22%3Atrue%2C%22directionsTarget%22%3A%22inline%22%2C%22scrollwheel%22%3Afalse%2C%22draggable%22%3Atrue%2C%22layers%22%3A%5B%5D%2C%22width%22%3A%22auto%22%2C%22height%22%3A%22550%22%2C%22panelEnabled%22%3Atrue%2C%22panelOpenByDefault%22%3Atrue%2C%22panelSearchVisible%22%3Atrue%2C%22panelSearchBy%22%3A%22location%22%2C%22panelSearchPlaceholder%22%3A%22%22%2C%22panelListItemElements%22%3A%5B%22title%22%2C%22category%22%2C%22image%22%2C%22address%22%2C%22phone%22%2C%22workingHours%22%2C%22email%22%2C%22description%22%5D%2C%22mainColor%22%3A%22rgb%28169%2C%20137%2C%2070%29%22%2C%22style%22%3A%22retro%22%2C%22colorGeometry%22%3A%22rgba%28235%2C227%2C205%2C1%29%22%2C%22colorLabelsTextFill%22%3A%22rgba%2882%2C55%2C53%2C1%29%22%2C%22colorLabelsTextStroke%22%3A%22rgba%28245%2C241%2C230%2C1%29%22%2C%22colorAdministrativeGeometryStroke%22%3A%22rgba%28201%2C178%2C166%2C1%29%22%2C%22colorAdministrativeLandParcel%22%3A%22rgba%28174%2C158%2C144%2C1%29%22%2C%22colorLandscapeNaturalGeometry%22%3A%22rgba%28223%2C210%2C174%2C1%29%22%2C%22colorPoiGeometry%22%3A%22rgba%28223%2C210%2C174%2C1%29%22%2C%22colorPoiLabelsTextFill%22%3A%22rgba%28147%2C129%2C124%2C1%29%22%2C%22colorPoiParkGeometryFill%22%3A%22rgba%28165%2C176%2C118%2C1%29%22%2C%22colorPoiParkLabelsTextFill%22%3A%22rgba%2868%2C117%2C48%2C1%29%22%2C%22colorRoadGeometry%22%3A%22rgba%28245%2C241%2C230%2C1%29%22%2C%22colorRoadArterial%22%3A%22rgba%28253%2C252%2C248%2C1%29%22%2C%22colorRoadHighway%22%3A%22rgba%28248%2C201%2C103%2C1%29%22%2C%22colorRoadHighwayGeometryStroke%22%3A%22rgba%28233%2C188%2C98%2C1%29%22%2C%22colorRoadHighwayControlledAccessGeometry%22%3A%22rgba%28233%2C141%2C88%2C1%29%22%2C%22colorRoadHighwayControlledAccessGeometryStroke%22%3A%22rgba%28219%2C133%2C85%2C1%29%22%2C%22colorRoadLocalLabelsTextFill%22%3A%22rgba%28128%2C107%2C99%2C1%29%22%2C%22colorTransitLineGeometry%22%3A%22rgba%28223%2C210%2C174%2C1%29%22%2C%22colorTransitLineLabelsTextFill%22%3A%22rgba%28143%2C125%2C119%2C1%29%22%2C%22colorTransitLineLabelsTextStroke%22%3A%22rgba%28235%2C227%2C205%2C1%29%22%2C%22colorTransitStationGeometry%22%3A%22rgba%28223%2C210%2C174%2C1%29%22%2C%22colorWaterGeometryFill%22%3A%22rgba%28185%2C211%2C194%2C1%29%22%2C%22colorWaterLabelTextFill%22%3A%22rgba%28146%2C153%2C141%2C1%29%22%2C%22customGoogleMapsStyles%22%3A%22.eapps-google-maps-bar-content-item-main%7B%5Cnbackground%3A%20%23%23f3f3f3%3B%5Cn%7D%22%2C%22apiKey%22%3A%22AIzaSyA5V1zo2vBox3bfNFKL83ACRYDVyAXWUV8%22%2C%22widgetId%22%3A%221%22%7D"

# Step 1: Decode the URL-encoded data
decoded_data = urllib.parse.unquote(url_encoded_data)

# Step 2: Load the JSON structure
data = json.loads(decoded_data)

# Step 3: Extract the coordinates for each marker
coordinates = []

for marker in data['markers']:
    name = marker['infoTitle']
    coordinates_str = marker['coordinates']
    lat, lon = map(float, coordinates_str.split(','))
    coordinates.append({'name': name, 'Latitude': lat, 'Longitude': lon})

# Step 4: Print the coordinates for each agency
for coord in coordinates:
    print(f"Agency: {coord['name']}, Latitude: {coord['Latitude']}, Longitude: {coord['Longitude']}")

country_data={}
country_data['cotedivoire'] = coordinates

with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/versus-bank/versus.json', 'w', encoding='utf-8') as f:
    json.dump(country_data, f, indent=4)
"""
import json
with open('civ/versus-bank/versus.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

civ_data=[]
for branch in data['cotedivoire']:
    civ_data.append({
        "bank": "versus_bank",
        "country": "civ",
        "address": branch["name"][:80],
        "Latitude": branch["Latitude"],
        "Longitude": branch["Longitude"],
        "geocoded": 0
    })

with open('result/json_data_all/versus_bank.json', 'w', encoding='utf-8') as f:
    json.dump(civ_data, f, ensure_ascii=False, indent=4)

"""
import pandas as pd

df = pd.DataFrame(data['cotedivoire'])


import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/civ/versus-bank/versus.shp')"""