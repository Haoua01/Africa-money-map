'''import requests
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from urllib.parse import unquote 
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent



"""
countries=["benin", "burkina", "cote-divoire", "guinee-bissau", "mali", "niger", "senegal", "togo"]

# Create an empty dictionary to store country data
country_data = {}
# Loop through each country to scrape data
for country in countries:
    data=[]
    print(f"Scraping data for {country}...")
    url = f"https://www.orabank.net/fr/filiale/{country}/reseau-dagences"

    # Set up ChromeDriver service
    service = Service('/Users/haouabenaliabbo/Downloads/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # Find all divs with class 'info_ouverture'
    branch_containers = driver.find_elements(By.CLASS_NAME, 'info_ouverture')

    # Loop through each branch container
    for container in branch_containers:
        try:
            header_tag = container.find_element(By.XPATH, ".//preceding-sibling::h2").text
            location = container.find_element(By.CLASS_NAME, 'addr').text
            opening_hours = container.find_element(By.CLASS_NAME, 'office-hours__item').text
            phone_number = container.find_element(By.CLASS_NAME, 'phone_fax').text

            # Find the Google Maps link for each branch
            google_maps_link_tag = container.find_element(By.XPATH, ".//a[contains(@href, 'https://maps.google.com/maps?daddr=')]")
            google_maps_link = google_maps_link_tag.get_attribute('href')

            # Clean the link by removing newlines and extra spaces
            google_maps_link = google_maps_link.replace("\n", "").replace(" ", "")
            google_maps_link = unquote(google_maps_link)
            # Extract latitude and longitude from the cleaned URL
            lat_lon = google_maps_link.split('=')[1]  # This gives the "latitude,longitude"
            if ',' in lat_lon:
                latitude, longitude = lat_lon.split(', ')
            else:
                latitude, longitude = None, None

            # Store the data in the dictionary
            data.append({
                "Name": header_tag,
                "Location": location,
                "Opening Hours": opening_hours,
                "Phone Number": phone_number,
                "Latitude": latitude,
                "Longitude": longitude,
            })
        except Exception as e:
            print(f"Error extracting data for branch {header_tag}: {e}")

    country_data[country] = data
    
    # Close the browser session after scraping
    driver.quit()




#create a directory to save the json file
os.makedirs("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/orabank", exist_ok=True)

#save as a json file
with open("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/result/orabank/orabank.json", "w") as f:
    json.dump(country_data, f, indent=4)


#if Name starts with "Agence" then get Latitude and Longitude as a csv file
data = []

for country, country_info in country_data.items():
    for branch in country_info:
        if branch["Name"].startswith("Agence"):
            data.append({
                "Latitude": branch["Latitude"],
                "Longitude": branch["Longitude"]
            })

df = pd.DataFrame(data)
print(df.head())
"""
'''
import json

#open json file orabank_corrected.json and extract latitude and longitude into a shapefile
with open("result/orabank/orabank_corrected.json", "r") as f:
    orabank_data = json.load(f)

data = []

for country, country_info in orabank_data.items():
    for branch in country_info:
        if branch["Name"].startswith("Agence"):
            data.append({
                'bank': "orabank",
                'country': country,
                'address': branch['Location'][:80],
                "Latitude": float(branch["Latitude"]),
                "Longitude": float(branch["Longitude"]),
                "geocoded": 0
            })
with open("result/json_data_all/orabank.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""
df = pd.DataFrame(data)

#save geolocations to a shapefile
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)



gdf.to_file("/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/GitHub/Scrapping-banks/UEMOA/result/orabank/orabank.shp")
"""