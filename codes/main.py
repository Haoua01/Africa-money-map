#define main function to run department_data.py
from department_data import DepartmentData
from commune_data import CommuneData
from region_data import RegionData

import geopandas as gpd

def main():
    commune_data = CommuneData('/Users/haouabenaliabbo/Desktop/M2 IREN/ALTERNANCE/Africa Money Map/Africa-money-map/data/CEMAC/tchad_communes.shp')
    commune_data.compute_scores(calculation_type='base')
    #department_data = DepartmentData('Africa-money-map/data/CEMAC/cameroun_communes_scores_threshold_50000_alpha.shp')
    #region_data = RegionData('data/Ghana/communes_scores_threshold_50000_alpha.shp')
    
    # Compute mean scores for departments
    #shp_department = gpd.read_file('Africa-money-map/data/CEMAC/cameroun_departments.shp')
    #department_data.compute_mean_scores(shp_department)
    #shp_region = gpd.read_file('data/Ghana/regions.shp')
    #region_data.compute_mean_scores(shp_region)
    
    #print("Region data processing complete.")

if __name__ == "__main__":
    main()
