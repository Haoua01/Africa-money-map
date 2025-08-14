import pandas as pd
import json
from geopandas import GeoDataFrame
from shapely.geometry import Point


with open('/workspaces/Africa-money-map/codes/Scraping/branches_combined.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)
gdf.crs = "EPSG:4326"  

gdf.to_file('/workspaces/Africa-money-map/codes/Scraping/branches_combined.shp')