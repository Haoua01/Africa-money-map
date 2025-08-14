from shapefile import Shapefile
import json
import numpy as np
from utils import normalize_scores, format_scores
#from geopy.distance import great_circle


class CommuneData(Shapefile):

    #THRESHOLD = 50000 #tchad=100000
    ALPHA = 1.01 #same for all countries 1.0001 except for Nigeria

    def __init__(self, shp, alpha=ALPHA):
        super().__init__(shp)
        self.shp = self.load_shapefile()
        self.alpha = alpha
        self.countries = self.data['Country'].unique()
        self.branch_counts = self.get_branch_count()
        #self.population = self.get_population()


        
    '''
    def compute_neighbors(self):
        """Compute neighbors for communes based on geographical distance."""
        neighbors = {}
        for country in self.countries:
            neighbors[country] = {}
            country_data = self.data[self.data['Country'] == country]
            for _, row1 in country_data.iterrows():
                city1_id = row1['UniqueID']  # Use a unique identifier for the city
                city1_name = row1['ADM3_FR']
                coords1 = (row1['Latitude'], row1['Longitude'])
                neighbors[country][city1_name] = {}
                for _, row2 in country_data.iterrows():
                    city2_id = row2['UniqueID']  # Use a unique identifier for the city
                    city2_name = row2['ADM3_FR']
                    coords2 = (row2['Latitude'], row2['Longitude'])
                    if city1_id != city2_id:
                        distance = great_circle(coords1, coords2).kilometers
                        if distance <= self.threshold:
                            neighbors[country][city1_name][city2_name] = distance
        self.neighbors = neighbors  # Store neighbors in self.neighbors
        with open(f'data/{area}/neighbors_threshold_{self.threshold}.json', 'w', encoding='utf-8') as f:
            json.dump(neighbors, f, ensure_ascii=False, indent=4)
        return neighbors
    '''

    def create_distance_dict(self,data):
        """
        Creates a nested dictionary where the key is city1 (InputID) and the value is 
        another dictionary with city2 (TargetID) as the key and the distance as the value.
        
        :param data: List of features containing 'InputID', 'TargetID', and 'Distance'
        :return: Nested dictionary
        """
        distance_dict = {}

        # Loop through each feature in the dataset
        for feature in data:
            city1 = feature["properties"]["InputID"]  # City1 (key)
            city2 = feature["properties"]["TargetID"]  # City2
            distance = feature["properties"]["Distance"]  # Distance between city1 and city2

            if city1 not in distance_dict:
                distance_dict[city1] = {}
            distance_dict[city1][city2] = distance
        print(f"Distance dictionary created with {len(distance_dict)} entries.")

        return distance_dict

    
    def compute_scores(self, threshold, area, alpha, calculation_type, adm_type):
        isibf_values = {}
        isibf = {}
        #neighbors_uemoa = {}
        #print(self.branch_counts)

        # Calculate ISIBF values for each country
        for country in self.countries:
            #neighbors_uemoa[country] = {}
            isibf_values[country] = {}
            print(f"Calculating ISIBF values for {country}...")


            #with open(f'data/{area}/{country}_distance_matrix.json',  'r') as f:
                #neighbors_raw = [json.loads(line) for line in f if line.strip()]

            #neighbors = self.create_distance_dict(neighbors_raw)

            #with open(f'data/{area}/{country}_distance_matrix_clean.json', 'w', encoding='utf-8') as f: 
                #json.dump(neighbors, f, ensure_ascii=False, indent=4)

            with open(f'/workspaces/Africa-money-map/data/ORS/{country}_ors_distance_matrix_in_seconds.json', 'r', encoding='utf-8') as f:
            #with open(f'/workspaces/Africa-money-map/data/UEMOA/{country}_distance_matrix_clean.json', 'r', encoding='utf-8') as f:
                neighbors = json.load(f)
            
            # Filter the shapefile for the specific country
            country_shp = self.shp[self.shp['Country'] == country]
            
            # Calculate ISIBF values for each city in the country
            for city in country_shp['ADM3_FR']:
                #neighbors_uemoa[country][city] = {}
                own_contribution = 0
                neighbors_contributions = 0
                if calculation_type == 'base':
                    # Branch-based calculation only
                    for neighbor, distance in neighbors.get(city, {}).items():
                        #print(f"Processing neighbor {neighbor} for city {city} in {country} with distance {distance}")
                        if distance/60 <= 90:
                            neighbors_contributions += np.log2(self.branch_counts[neighbor]+1) / (self.alpha ** (distance/60))
                        #if city == 'Lolobo':
                            #print(f"Neighbor {neighbor} for city {city} in {country}: Distance = {distance/60} minutes, Contribution = {np.log2(self.branch_counts[neighbor] + 1) / (self.alpha ** (distance/60))}")
                            #neighbors_uemoa[country][city][neighbor] = distance
                    own_contribution += np.log2(self.branch_counts[city] +1)

                isibf_values[country][city] = own_contribution + neighbors_contributions
                if city=='Mopti':
                    print(f"ISIBF value for {city} in {country}:  {self.branch_counts[city]}, {own_contribution}, {neighbors_contributions}, {isibf_values[country][city]}")
                #print(f"ISIBF value for {city} in {country}: {isibf_values[country][city]}")

            if adm_type == 'communes':
                isibf[country] = format_scores(normalize_scores(isibf_values[country]))
            elif adm_type == 'mean_communes':
                isibf[country] = isibf_values[country]

        # Map ISIBF values to the shapefile
        #for country in self.countries:
            #neighbors_uemoa[country] = {
                #city: neighbors for city, neighbors in neighbors_uemoa[country].items() if neighbors
            #}
            #country_shp = self.shp[self.shp['Country'] == country]
            #for city in country_shp['ADM3_FR']:
                #if city in neighbors_uemoa[country]:
                    #self.shp.loc[self.shp['ADM3_FR'] == city, f'Filter'] = int(1)
                #else:
                    #self.shp.loc[self.shp['ADM3_FR'] == city, f'Filter'] = int(0)
            #self.shp.loc[self.shp['Country'] == country, f'ISIBF_{calculation_type}'] = country_shp['ADM3_FR'].map(isibf[country])

        for country in self.countries:
            country_shp = self.shp[self.shp['Country'] == country]
            for city in country_shp['ADM3_FR']:
                #print(f"Before saving - Branch count for {city}: {self.branch_counts.get(city, 'Not Found')}")
                self.shp.loc[self.shp['Country'] == country, f'ISIBF_{calculation_type}'] = country_shp['ADM3_FR'].map(isibf[country])
                self.shp.loc[self.shp['Country'] == country, f'ISIBF_raw'] = country_shp['ADM3_FR'].map(isibf_values[country])



        output_path = f'/workspaces/Africa-money-map/data/scores_time_travels_alpha_1_01.shp'
        
        #define the output path for the shapefile
        #if country=='cameroun' and adm_type=='communes':
            #output_path = f'data/{area}/scores_{adm_type}_{country}.shp'
        #elif country=='cameroun' and adm_type=='mean_communes':
            #output_path = f'data/{area}/scores_{adm_type}_{country}.shp'
        #elif country=='tchad':
            #output_path = f'data/{area}/scores_{adm_type}_{country}.shp'
        #else:
            #output_path = f'data/{area}/scores_{adm_type}.shp'
        self.shp.to_file(output_path)
        print('ISIBF values calculated')

        #with open('/workspaces/Africa-money-map/data/ORS/all_neighbors_equipped_clean.json', 'w', encoding='utf-8') as f:
            #json.dump(neighbors_uemoa, f, ensure_ascii=False, indent=4)
        #print(f"Neighbors data saved to /workspaces/Africa-money-map/data/ORS/all_neighbors_equipped_clean.json")

        return output_path

