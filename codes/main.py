#define main function to run department_data.py
from department_data import DepartmentData
from commune_data import CommuneData
from region_data import RegionData

import geopandas as gpd

threshold_uemoa = {
    "benin":50000,
    "burkina":50000,
    'civ':50000,
    'guinee':50000,
    'mali':100000,
    'niger':100000,
    'senegal':50000,
    'togo':50000,
}

threshold_CEMAC = {
    "cameroun": 50000,
    "tchad": 100000
}

threshold_ghana = {
    "ghana":50000
}

shp_area = {
        'CEMAC':{
        'tchad':
        {
            'adm2':'Africa-money-map/data/CEMAC/tchad_communes.shp',
        },
        'cameroun':
        {
            'adm3':'Africa-money-map/data/CEMAC/cameroun_communes.shp',
            'adm2':'Africa-money-map/data/CEMAC/cameroun_departments.shp',
        }
    },
        'Ghana': 
        {
            'adm2':'Africa-money-map/data/Ghana/ghana_communes.shp'
        },
    'UEMOA': {
        'adm3':'Africa-money-map/data/UEMOA/communes_with_id.shp',
        'adm2':'Africa-money-map/data/UEMOA/departments.shp'
    }
}

def main():
    for area, shp_files in shp_area.items():
        print(area)
        if area == 'UEMOA':
            shp_communes=shp_files['adm3']
            shp_departments=gpd.read_file(shp_files['adm2'])
            commune_data = CommuneData(shp=shp_communes)
            shp_communes_scores = commune_data.compute_scores(threshold=threshold_uemoa, area=area, calculation_type='base', adm_type='communes')
            path_shp_communes = commune_data.compute_scores(threshold=threshold_uemoa, area=area, calculation_type='base', adm_type='mean_communes')
            department_data = DepartmentData(shp=path_shp_communes)
            shp_departments_scores = department_data.compute_mean_scores(shp_departments, area=area)
        elif area == 'CEMAC':
            for country, shp_files_country in shp_files.items():
                print(country)
                if country == 'tchad':
                    shp_communes = shp_files_country['adm2']
                    commune_data = CommuneData(shp=shp_communes)
                    shp_communes_scores = commune_data.compute_scores(threshold=threshold_CEMAC, area=area, calculation_type='base', adm_type='communes')
                elif country == 'cameroun':
                    shp_communes=shp_files_country['adm3']
                    shp_departments=gpd.read_file(shp_files_country['adm2'])
                    commune_data = CommuneData(shp=shp_communes)
                    #shp_communes_scores = commune_data.compute_scores(threshold=threshold_CEMAC, area=area, calculation_type='base', adm_type='communes')
                    path_shp_communes = commune_data.compute_scores(threshold=threshold_CEMAC, area=area, calculation_type='base', adm_type='mean_communes')
                    department_data = DepartmentData(shp=path_shp_communes)
                    shp_departments_scores = department_data.compute_mean_scores(shp_departments, area=area)
        elif area == 'Ghana':
            shp_communes = shp_files['adm2']
            commune_data = CommuneData(shp=shp_communes)
            shp_communes_scores = commune_data.compute_scores(threshold=threshold_ghana, area=area, calculation_type='base', adm_type='communes')


    #commune_data = CommuneData(shp='Africa-money-map/data/Ghana/ghana_communes.shp')
    #commune_data.compute_scores(threshold=threshold_uemoa, area='UEMOA', calculation_type='base')
    #department_data = DepartmentData('Africa-money-map/data/Ghana/Ghana_communes_scores.shp')
    #region_data = RegionData('data/Ghana/communes_scores_threshold_50000_alpha.shp')
    
    # Compute mean scores for departments
    #shp_department = gpd.read_file('Africa-money-map/data/Ghana/Ghana_departments.shp')
    #department_data.compute_mean_scores(shp_department)
    #shp_region = gpd.read_file('data/Ghana/regions.shp')
    #region_data.compute_mean_scores(shp_region)
    
    #print("Region data processing complete.")

if __name__ == "__main__":
    main()
