"""
import requests
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

url = "https://www.ecobank.com/source_pages/MapHandler.ashx"

country_and_code = {
    "BJ":"bj",
    "CI":"ci",
    "BF":"bf",
    "GW":"gw",
    "ML":"ml",
    "NE":"ne",
    "SN":"sn",
    "TG":"tg"

}

country_data = {}

for country, code in country_and_code.items():
    payload = "method=get_markers&btype=3&ccode="+country
    headers = {
        #"cookie": "ASP.NET_SessionId=2ukyjm3d1jeztugzs500yg0i; theme=default",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        #"Cookie": "theme=default; language=fr; languageFeedback=fr; ai_user=zxNWT|2024-11-12T19:23:52.494Z; _fbp=fb.1.1731439432587.16643094818176793; current_country=CI; ASP.NET_SessionId=oadnrrv11jpv3puldzul13i4; _gid=GA1.2.294730376.1737459850; dtCookie=v_4_srv_2_sn_1B2922BAED9FF8255184983958C824F0_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0; _ga_F8LYDKHJ57=GS1.1.1737463801.6.1.1737464462.59.0.0; _ga=GA1.2.462355508.1731439432; _gat=1; ai_session=DT+VC|1737463802785|1737464462509.5",
        "Origin": "https://www.ecobank.com",
        "Pragma": "no-cache",
        "Referer": "https://www.ecobank.com/"+code+"/personal-banking/contact-us/locator",
        #"Request-Id": "|Lyier.nr1Ly",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\""
    }

    r = requests.request("POST", url, data=payload, headers=headers)

    country_data[code] = r.json()

print(country_data)

#save as json
import json
import os

#create a directory to save the json file
os.makedirs("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result", exist_ok=True)

#save as a json file
#with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/ecobank.json", "w") as f:
    #json.dump(country_data, f, indent=4)




#keep "Latitude", "Longitude" and save to a csv file
"""
country_and_code = {
    "bj":"benin",
    "ci":"civ",
    "bf":"burkina",
    "gw":"guinee",
    "ml":"mali",
    "ne":"niger",
    "sn":"senegal",
    "tg":"togo"

}

import pandas as pd
import json

with open('result/ecobank/ecobank.json', "r", encoding="utf-8") as f:
    ecobank_data = json.load(f)

data = []

for country, country_info in ecobank_data.items():
    for atm in country_info:
        data.append({
            "bank": "ecobank",
            "country": country_and_code[country],
            "address": (atm['AgenceAdresse']+ ', '+ atm['Branch_area'])[:80],
            "Latitude": atm["Latitude"],
            "Longitude": atm["Longitude"],
            "geocoded":0
        })

with open('result/json_data_all/ecobank.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/ecobank/ecobank.shp")
"""