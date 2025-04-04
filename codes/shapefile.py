import geopandas as gpd

class Shapefile:
    def __init__(self, filename):
        self.filename = filename
        self.data = gpd.read_file(filename)

    def load_shapefile(self):
        return self.data
    
    def get_commune_attribute(self, attribute_column):
        """Create a dictionary of commune attributes (e.g., coordinates, population) from the shapefile data."""
        commune_attribute = {}
        for index, row in self.data.iterrows():
            commune = row['ADM3_FR']
            attribute_value = row[attribute_column]
            commune_attribute[commune] = attribute_value
        return commune_attribute

    
    def get_scores_mapping(self, key_column, value_column, calculation_type):
        mapping = {}
        for _, row in self.data.iterrows():
            country = row['Country']
            key = row[key_column]  
            value = row[value_column]  
            score = row[f'ISIBF_{calculation_type}']
            if country not in mapping:
                mapping[country] = {}
            if key not in mapping[country]:
                mapping[country][key] = {}
            mapping[country][key][value] = score
        return mapping

    def get_coordinates(self):  
        return self.get_commune_attribute('Coordinates')  

    def get_population(self):
        return self.get_commune_attribute('Population')
    
    def get_area(self):
        return self.get_commune_attribute('Area')
    
    def get_density(self):
        return self.get_commune_attribute('Density')
    
    def get_density_class_gcd(self):
        return self.get_commune_attribute('GCD')
    
    def get_branch_count(self):
        return self.get_commune_attribute('Total_bran')

    def get_department_mapping(self, calculation_type):
        return self.get_scores_mapping('ADM2_FR', 'ADM3_FR', calculation_type)
    
    def get_region_mapping(self, calculation_type):
        return self.get_scores_mapping('ADM1_FR', 'ADM3_FR', calculation_type)
    
    def get_country_mapping(self, calculation_type):
        return self.get_scores_mapping('ADM0_FR', 'ADM3_FR', calculation_type)
    
    
    
