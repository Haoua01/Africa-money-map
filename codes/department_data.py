from shapefile import Shapefile
import numpy as np
from utils import normalize_scores, format_scores

class DepartmentData(Shapefile):
    def __init__(self, shp):
        super().__init__(shp)
        self.shp = self.load_shapefile()
        self.scores_mapping = self.get_department_mapping(calculation_type='base')
        self.countries = self.shp['Country'].unique()

    def compute_mean_scores(self, shp_department):
        mean_scores = {}
        for country, departments in self.scores_mapping.items():
            mean_scores[country] = {}
            for department, communes in departments.items():
                total_score = 0
                count = 0
                for commune, score in communes.items():
                    total_score += score
                    count += 1
                mean_scores[country][department] = total_score / count if count > 0 else 0
        normalized_scores = {}
        for country, departments in mean_scores.items():
            normalized_scores[country] = normalize_scores(departments) 
        for country, departments in normalized_scores.items():
            for department, normalized_score in departments.items():
                # Update the 'ISIBF_base' column for the corresponding department
                shp_department.loc[shp_department['ADM2_FR'] == department, 'ISIBF_base'] = normalized_score


        # Save the updated shapefile
        output_path = 'data/UEMOA/departments_scores_alpha.shp'
        shp_department.to_file(output_path)

        print(f'ISIBF values added and saved to {output_path}')

