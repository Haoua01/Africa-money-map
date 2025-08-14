import numpy as np
import json
from utils import normalize_scores, format_scores
from shapefile import Shapefile

class IndicatorCalculator(Shapefile):
    
    def __init__(self, alpha=1.01):
        super().__init__()
        self.alpha = alpha
        self.neighbors = None  # Initialize the neighbors attribute

    def compute_neighbors(self, threshold=200):
        """Compute neighbors for communes based on geographical distance."""
        from geopy.distance import great_circle
        neighbors = {}
        for country in self.countries:
            neighbors[country] = {}
            country_data = self.data[self.data['Country'] == country]
            for _, row1 in country_data.iterrows():
                city1 = row1['ADM3_FR']
                coords1 = (row1['Latitude'], row1['Longitude'])
                neighbors[country][city1] = {}
                for _, row2 in country_data.iterrows():
                    city2 = row2['ADM3_FR']
                    coords2 = (row2['Latitude'], row2['Longitude'])
                    if city1 != city2:
                        distance = great_circle(coords1, coords2).kilometers
                        if distance <= threshold:
                            neighbors[country][city1][city2] = distance
        self.neighbors = neighbors  # Store neighbors in self.neighbors
        with open('neighbors.json', 'w') as f:
            json.dump(neighbors, f)
        return neighbors

    def calculate_isibf_shp(self, shp, calculation_type):
        isibf_values = {}
        isibf_norm = {}
        
        # Ensure neighbors are computed
        if self.neighbors is None:
            self.compute_neighbors()

        # Calculate ISIBF values for each country
        for country in self.countries:
            isibf_values[country] = {}
            
            # Filter the shapefile for the specific country
            country_shp = shp[shp['Country'] == country]
            
            # Calculate ISIBF values for each city in the country
            for city in country_shp['ADM3_FR']:
                own_contribution = 0
                neighbors_contributions = 0
                if city in self.branch_counts:
                    if calculation_type == 'pop':
                        # Population-based calculation
                        for neighbor, distance in self.neighbors.get(country, {}).get(city, {}).items():
                            if distance > 0:
                                neighbors_contributions += np.log2((self.branch_counts[neighbor]/self.population[neighbor]) + 1) / self.alpha ** distance
                        own_contribution = np.log2((self.branch_counts[city]/self.population[city]) + 1)
                    elif calculation_type == 'base':
                        # Branch-based calculation
                        for neighbor, distance in self.neighbors.get(country, {}).get(city, {}).items():
                            if distance > 0:
                                neighbors_contributions += np.log2(self.branch_counts[neighbor] + 1) / self.alpha ** distance
                        own_contribution = np.log2(self.branch_counts[city] + 1)

                    isibf_values[country][city] = own_contribution + neighbors_contributions

            # Apply normalization by country
            isibf_norm[country] = format_scores(normalize_scores(isibf_values[country]))

        # Map ISIBF values to the shapefile
        for country in self.countries:
            # Filter the shapefile for the specific country
            country_shp = shp[shp['Country'] == country]
            
            # Map ISIBF values to communes
            shp.loc[shp['Country'] == country, f'ISIBF_{calculation_type}'] = country_shp['ADM3_FR'].map(isibf_norm[country])

        # Save the updated shapefile
        shp.to_file('data/communes_scores.shp')
        print('ISIBF values calculated and added to shapefile.')
