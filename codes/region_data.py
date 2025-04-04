from shapefile import Shapefile
import numpy as np
from utils import normalize_scores, format_scores

class RegionData(Shapefile):
    def __init__(self, shp):
        super().__init__(shp)
        self.shp = self.load_shapefile()
        self.scores_mapping = self.get_region_mapping(calculation_type='base')
        self.countries = self.shp['Country'].unique()
        
    def compute_mean_scores(self, shp_region):
        mean_scores = {}

        # Calculate mean scores for each region
        for country, regions in self.scores_mapping.items():
            mean_scores[country] = {}
            for region, communes in regions.items():
                total_score = 0
                count = 0
                for commune, score in communes.items():
                    total_score += score
                    count += 1
                mean_scores[country][region] = total_score / count if count > 0 else 0
                #shp_region.loc[shp_region['ADM1_FR'] == region, 'ISIBF_base'] = mean_scores[country][region]
        normalized_scores = {}
        for country, regions in mean_scores.items():
            normalized_scores[country] = format_scores(normalize_scores(mean_scores[country]))
        for country, regions in normalized_scores.items():
            for region, normalized_score in regions.items():
                shp_region.loc[shp_region['ADM1_FR'] == region, 'ISIBF_base'] = normalized_score

        # Save the updated shapefile
        output_path = 'data/UEMOA/regions_scores_alpha.shp'
        shp_region.to_file(output_path)

        print(f'ISIBF values added and saved to {output_path}')

