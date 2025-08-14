import requests
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

url1 = "https://umap.openstreetmap.fr/fr/datalayer/462104/37f3d4df-3f9b-4e30-84ff-8d6ab8e2efbe"
url2 = "https://umap.openstreetmap.fr/fr/datalayer/462104/e998bc05-061d-4ede-9d8a-1f7e9e3a8433"

urls=[url1,url2]
civ_data = {}
branch_data = []

data=[]

for url in urls:
    payload = ""
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://umap.openstreetmap.fr/fr/map/agences-nsia-banque-ci_462104?scaleControl=false&miniMap=true&scrollWheelZoom=true&zoomControl=true&allowEdit=false&moreControl=false&searchControl=null&tilelayersControl=false&embedControl=false&datalayersControl=true&onLoadPanel=databrowser&captionBar=false&fullscreenControl=false&locateControl=true&measureControl=false&editinosmControl=false",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    r = requests.request("GET", url, data=payload, headers=headers)
    branch_data = r.json()
    for branch in branch_data["features"]:
        agency_name = branch["properties"]["name"]
        address = branch["properties"]["description"]
        latitude = branch["geometry"]["coordinates"][1]
        longitude = branch["geometry"]["coordinates"][0]
        data.append({
            "agency_name": agency_name,
            "address": address,
            "Latitude": latitude,
            "Longitude": longitude
        })

civ_data["cotedivoire"]=data





#save to a json file

with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/nsia/nsia_civ.json", "w") as f:
    json.dump(civ_data, f, indent=4)