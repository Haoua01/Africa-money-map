#define main function to run department_data.py
from department_data import DepartmentData
from commune_data import CommuneData
from region_data import RegionData

import geopandas as gpd

def main():
    commune_data = CommuneData('data/UEMOA/communes_with_id.shp')
    commune_data.compute_scores(calculation_type='base')
    department_data = DepartmentData('data/UEMOA/communes_scores_threshold_50000_alpha.shp')
    region_data = RegionData('data/UEMOA/communes_scores_threshold_50000_alpha.shp')
    
    # Compute mean scores for departments
    shp_department = gpd.read_file('data/UEMOA/departments.shp')
    department_data.compute_mean_scores(shp_department)
    shp_region = gpd.read_file('data/UEMOA/regions.shp')
    region_data.compute_mean_scores(shp_region)
    
    print("Region data processing complete.")

if __name__ == "__main__":
    main()
