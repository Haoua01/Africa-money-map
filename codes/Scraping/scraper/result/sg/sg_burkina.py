
'''import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import os
import pandas as pd
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent



"""
country_and_code = {
    "benin":"https://societegenerale.bj/fr/nous-connaitre/nos-implantations/",
    "burkina-faso":"https://societegenerale.bf/fr/implantations/country/burkina-faso/",
    "coteivoire":"https://particuliers.societegenerale.ci/fr/devenir-client/nos-agences/",
    "senegal":"https://societegenerale.sn/fr/nous-connaitre/notre-reseau-dagences/",
    "togo":"https://societegenerale.tg/fr/contact/nos-agences/"
}

country_data = {}
for country, key in country_and_code.items():
    # URL of the page that contains the JavaScript object
    url = key


    # Set up ChromeDriver service
    service = Service('/Users/haouabenaliabbo/Downloads/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(3)

    # Extract the entire script containing the JSON data using XPath
    # Look for the script tag that contains the "countryList" and "implantationsList"
    script = driver.find_element(By.XPATH, "//script[contains(text(), 'implantationsList')]").get_attribute("innerHTML")

    # Now extract the JSON from the script
    start_index = script.find('implantationsList = [') + len('implantationsList = ')
    end_index = script.find('];', start_index) + 1
    json_data = script[start_index:end_index]

    # Parse the JSON data
    implantations_list = json.loads(json_data)
        
    country_data[country] = implantations_list
    # Close the WebDriver
    driver.quit()


#create a directory to save the json file
os.makedirs("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/sg", exist_ok=True)

"""
'''
import json
#save as a json file
with open('result/sg/sg_corrected.json', "r") as f:
    country_data2=json.load(f)


for country, country_info in country_data2.items():
    print(country)
    for branch in country_info:

        branch["coordX"] = branch["coordX"].replace(" ", "")
        branch["coordY"] = branch["coordY"].replace(" ", "")

#if Name starts with "Agence" then get Latitude and Longitude as a csv file
data = []

for country, country_info in country_data2.items():
    for branch in country_info:
        data.append({
            "bank": "sg",
            "country": country,
            "address": branch["adr1"][:88],
            "Latitude": branch["coordX"],
            "Longitude": branch["coordY"],
            "geocoded": 0
        })

with open('result/json_data_all/sg.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
"""
df = pd.DataFrame(data)
print(df.head())


#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)

gdf.to_file('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/sg/sg.shp')
"""