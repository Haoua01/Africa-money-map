import folium
from shapely.geometry import shape
import os 
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from branca.colormap import LinearColormap

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import folium
from folium.features import CustomIcon
import matplotlib.colors as mcolors



class MapVisualizer:
    def __init__(self, geo_data, geo_borders, scores, adm_type, lat, lon, zoom, area):
        self.geo_data = geo_data
        self.geo_borders = geo_borders
        self.lat = lat
        self.lon = lon
        self.zoom = zoom
        self.scores = scores
        self.adm_type = adm_type
        self.area = area

    def generate_legend(num_colors):
    # dynamically generate a color map
        cmap = plt.get_cmap('viridis', num_colors)
        colors = [cmap(i) for i in range(cmap.N)]
        
        # generate labels based on how many colors there are
        log_labels = np.logspace(0, num_colors, num=num_colors, base=10).astype(int)
        
        fig, ax = plt.subplots(figsize=(6, 0.6))
        font_size = 12
        line_width = 30 
        
        # create colors
        for i, color in enumerate(colors):
            plt.plot([i, i+1], [1, 1], color=color, solid_capstyle='butt', linewidth=line_width)
            plt.text(i+0.5, 0.5, f'{log_labels[i]}', ha='center', va='center', fontsize=font_size, transform=ax.transData)

        ax.set_xlim(0, num_colors)
        ax.set_ylim(0, 2)
        ax.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        plt.savefig('dynamic_legend.png', dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()

        # add legend to map
        m = folium.Map(location=[20, 0], zoom_start=2)
        legend_img = 'dynamic_legend.png'
        icon = CustomIcon(legend_img, icon_size=(600, 120))  # Adjust icon size as needed

        marker = folium.Marker(location=[-25, 0], icon=icon, popup='Legend')  # Adjust location as needed
        m.add_child(marker)

    def create_leaflet_commune(self):

        self.geo_data['geometry'] = self.geo_data['geometry'].apply(lambda x: shape(x).simplify(0.01))
        self.geo_data = self.geo_data[['geometry', 'ADM3_FR', 'ADM0_FR', 'ISIBF_base']]

        # Initialize a Folium map
        my_map = folium.Map(location=[self.lat, self.lon], zoom_start=self.zoom, scrollWheelZoom=False)
        jawg_access_token = os.getenv("JAWG_ACCESS_TOKEN")

        # Add Jawg Light tiles with the access token
        folium.TileLayer(
            tiles="https://{s}.tile.jawg.io/jawg-light/{z}/{x}/{y}.png?access-token=" + jawg_access_token,
            attr="Map data &copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors, &copy; <a href='https://jawg.io/'>Jawg</a>",
            name="Jawg Light"
        ).add_to(my_map)

        # Define the custom log scale breaks and colors
        #log_breaks = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 13 intervals
        #log_colors = ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081', '#810f7c', '#4d004b', '#7f0037', '#b10026', '#d7001f']  # 13 colors

        log_breaks = [0, 0.001, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6, 0.8, 1]  # 9 intervals
        log_colors = ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081', '#810f7c', '#4d004b', '#7f0037', '#b10026']  # 8 colors


        # Create a LinearColormap (this allows for a continuous color scale)
        log_cmap = LinearColormap(colors=log_colors, vmin=min(log_breaks), vmax=max(log_breaks))

        # Plot the map with a choropleth layer
        folium.Choropleth(
            geo_data=self.geo_data.__geo_interface__,
            name='choropleth',
            data=self.geo_data,
            columns=['ADM3_FR', 'ADM0_FR', 'ISIBF_base'],
            key_on='feature.properties.ADM3_FR',
            fill_color='Blues',
            fill_opacity=1,
            line_opacity=0.1,
            line_weight=0.1,
            legend_name='Score d\'accès',
            highlight=True,
            bins=log_breaks
        ).add_to(my_map)

        # Add a tooltip to display information
        folium.GeoJson(
            self.geo_data.__geo_interface__,
            style_function=lambda feature: {
                'fillColor': 'Blues' if feature['properties']['ISIBF_base'] is not None else 'gray',
                'color': 'grey',
                'weight': 0.1,
                'fillOpacity': 0,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['ADM3_FR', 'ADM0_FR', 'ISIBF_base'],
                aliases=[':', 'score:'],
                localize=True,
            )
        ).add_to(my_map)

        # Plot the borders with a choropleth layer
        c=folium.Choropleth(
            geo_data=self.geo_borders.__geo_interface__,
            name='choropleth2',
            data=self.geo_borders,
            columns=['Country'],
            key_on='feature.properties.Country',
            fill_opacity=0.8,
            line_opacity=0.7,
            line_weight=0.8,
            legend=False,
        )
        
        #remove second legend
        for key in c._children:
            if key.startswith('color_map'):
                del(c._children[key])
        c.add_to(my_map)



        # Save the map as an HTML file
        folium_map_path = f'Africa-money-map/data/results/leaflet/{self.area}_scores_{self.adm_type}_leaflet.html'
        my_map.save(folium_map_path)

        print(f"Leaflet commune map generated")