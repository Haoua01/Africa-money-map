import json
import geopandas as gpd 
from shapely.geometry import Point
from geopandas import GeoDataFrame

import pandas as pd

with open('/workspaces/Africa-money-map/data/Regression/citypopulation/uemoa_communes.json', 'r') as f:
    data = json.load(f)

data_clean = []
for country, info in data.items():
    data_clean.extend(info)


# Create a GeoDataFrame from the JSON data
df = pd.DataFrame(data_clean)
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = GeoDataFrame(df, geometry=geometry)
gdf.to_file('/workspaces/Africa-money-map/data/Regression/citypopulation/population_uemoa.shp')