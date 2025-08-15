import json
import geopandas as gpd 

import pandas as pd

with open('/workspaces/Africa-money-map/data/Regression/uemoa_communes.json', 'r') as f:
    data = json.load(f)

data_clean=[]
for city in data['objs']:
    data_clean.append({
        'Country': 'Ghana',
        'City': city['name'],
        'Latitude': city['lat'],
        'Longitude': city['lng'],
        'Population': city['pop'][-1],
        'Area': city['area']
    })

# Create a GeoDataFrame from the JSON data
df = pd.DataFrame(data_clean)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
gdf.to_file('/workspaces/Africa-money-map/data/Regression/communes_uemoa.shp')