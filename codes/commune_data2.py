from shapefile2 import Shapefile
import json
import numpy as np
from utils import normalize_scores, format_scores
from geopy.distance import great_circle


class CommuneData(Shapefile):

    #THRESHOLD = 50000 #tchad=100000
    ALPHA = 1.00000001 #same for all countries 1.0001 except for Nigeria

    def __init__(self, shp, alpha=ALPHA):
        super().__init__(shp)
        self.shp = self.load_shapefile()
        self.alpha = alpha
        #self.countries = self.data['Country'].unique()
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
            coun = feature["properties"]["Country"]

            if coun not in distance_dict:
                distance_dict[coun] = {}
            if city1 not in distance_dict[coun]:
                distance_dict[coun][city1] = {}
            distance_dict[coun][city1][city2] = distance
        print(f"Distance dictionary created with {len(distance_dict)} entries.")

        return distance_dict

    
    def compute_scores(self, threshold, area, calculation_type, adm_type, country):
        isibf_values = {}
        isibf = {}

        #with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/Juin/FCA/distance_countries.json',  'r') as f:
            #neighbors_raw = [json.loads(line) for line in f if line.strip()]

        #neighbors = self.create_distance_dict(neighbors_raw)

        #with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/Juin/FCA/distance_matrix_clean_countries.json', 'w', encoding='utf-8') as f: 
            #json.dump(neighbors, f, ensure_ascii=False, indent=4)

        with open('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/Bounie/Index2/distance_matrix_clean.json', 'r', encoding='utf-8') as f:
            neighbors = json.load(f)

        # Calculate ISIBF values for each country
        #for country in self.countries:
        isibf_values[country] = {}
        print(f"Calculating ISIBF values for {country}...")
        
        # Filter the shapefile for the specific country
        #country_shp = self.shp[self.shp['Country'] == country]
        country_shp = self.shp
        #neighbors_country= neighbors.get(country, {})

        
        # Calculate ISIBF values for each city in the country
        for city in country_shp['id']:
            own_contribution = 0
            neighbors_contributions = 0
            if city in self.branch_counts:
                if calculation_type == 'base':
                    for neighbor, distance in neighbors.get(str(int(city)), {}).items():
                        #print(f"City: {city}, Neighbor: {neighbor}, Distance: {distance}")
                        if distance <= threshold[country]:  # Compare distance with the threshold
                            branch_count = self.branch_counts.get(float(neighbor), 0.0)  # Default to 0.0 if neighbor not found
                            neighbors_contributions += np.log2(branch_count+1) / (self.alpha**distance)
                            print(f"Neighbor contribution for {neighbor} in {city}: {neighbors_contributions}")
                    own_contribution += self.branch_counts[city]

                isibf_values[country][city] = own_contribution + neighbors_contributions
                #print(f"ISIBF value for {city} in {country}: {isibf_values[country][city]}")

                #if calculation_type == 'pop':
                    # considering population in scores calculation
                    #for neighbor, distance in neighbors.get(city, {}).items():
                        #if distance <= self.threshold:
                            #neighbors_contributions += np.log2((self.branch_counts[neighbor]/self.population[neighbor]) + 1) / self.alpha ** distance
                    #own_contribution = np.log2((self.branch_counts[city]/self.population[city]) + 1)
                #if calculation_type == 'base':
                    # Branch-based calculation only
                    #for neighbor, distance in neighbors.get(city, {}).items():
                        #print(f"Processing neighbor {neighbor} for city {city}")
                        #if distance <= threshold[country]:
                            #neighbors_contributions += np.log2(self.branch_counts[neighbor] + 1) / self.alpha ** distance
                    #own_contribution += np.log2(self.branch_counts[city] + 1)


                #print(f"ISIBF value for {city} in {country}: {isibf_values[country][city]}")

        if adm_type == 'communes':
            isibf[country] = format_scores(normalize_scores(isibf_values[country]))
        elif adm_type == 'mean_communes':
            isibf[country] = isibf_values[country]

        # Map ISIBF values to the shapefile
        #for country in self.countries:
        #country_shp = self.shp[self.shp['Country'] == country]
        #self.shp.loc[self.shp['Country'] == country, f'ISIBF_{calculation_type}'] = country_shp['id'].map(isibf[country])
        country_shp = self.shp
        self.shp[f'ISIBF_{calculation_type}'] = country_shp['id'].map(isibf[country])
        output_path = '/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/Bounie/Index2/scores_13.shp'
        
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

        return output_path

