# Africa money map

This repository contains the datasets, code, and workflows used in this master’s thesis :
"Access to bank branches in West Africa: measurements and determinants".
The study develops and compares three spatial accessibility models to measure access to bank branches in West Africa, using a self-constructed geolocated dataset on bank branches.

## 1. Research Overview
We focus on the 8 countries of the West African Monetary Union: Benin, Burkina Faso, Ivory Coast, Guinea-Bissau, Mali, Niger, Senegal and Togo. 
We examined bank branch accessibility using geospatial data and socio-economic indicators.


### Indicators developed:
1. Floating Catchment Area (FCA)
    * Municipality-based accessibility measure.
    * Simple but limited: ~70% of municipalities score < 0.1 due to sparse coverage.
2. Isochrone-based Coverage
    * Travel-time polygons (15, 30, 45, 60 minutes) around branches, independent of boundaries.
    * Measures % of municipal area covered by at least one branch within non overlapping time travel ranges (0-15min, 15-30min, 30-45min, 45-60min).
    * Intuitive but fragmented when comparing municipalities.
3. Hybrid Approach (Preferred)
    * Combines FCA methodology with isochrone coverage.
    * Produces a single meaningful score for comparison.
    * Best balance between precision and interpretability.


### Key Findings:
* Access is concentrated in urban centers, rural areas remain underserved.
* Population density and share of adults in trade correlate positively with access.
* Lower education levels and higher shares of agricultural/self-employed workers correlate with lower access.

## 2. Codes and data

### Prerequisites
* Python 3.9+
* Docker 
* QGIS 
* Cloning of https://github.com/GIScience/openrouteservice.git
  
---

### Section 3.2 Data on bank branches
- Codes: 
    * Bank scraping and geocoding: [codes/Scraping/scraper](https://github.com/Haoua01/Africa-money-map/tree/main/codes/Scraping/scraper)
    * Combining data and shape file generation: [codes/Scraping/combine_json.py](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Scraping/combine_json.py) and [codes/Scraping/shapefile_generator.py](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Scraping/shapefile_generator.py)
- Data: [data/Scraping_data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Scraping_data)

---

### Section 3.3 Socio-economic data
- Codes: 
    * Household data cleaning is performed in QGIS 
    * citypopulation codes: [codes/Regression/citypopulation](https://github.com/Haoua01/Africa-money-map/tree/main/codes/Regression/citypopulation)
- Data: 
    * citypopulation data: [data/Regression/citypopulation](https://github.com/Haoua01/Africa-money-map/tree/main/data/Regression/citypopulation)
    * Regression: [data/Regression/data_regression.csv](https://github.com/Haoua01/Africa-money-map/blob/main/data/Regression/data_regression.csv)

---

### Section 4.1 Indicator 1: a Floating Catchment Area (FCA) model
- Codes: 
    * Distance matrix generation: [codes/ORS/ors_time_distance_matrix.py](https://github.com/Haoua01/Africa-money-map/blob/main/codes/ORS/ors_time_distance_matrix.py)
    * Index of access: [codes/FCA](https://github.com/Haoua01/Africa-money-map/tree/main/codes/FCA)
- Data: [data/Indicators/FCA](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/FCA)

---

### Section 4.2 Indicator 2: a fully isochrones approach
- Codes:
    * Isochrone generation: [codes/ORS/ors_isochrones.py](https://github.com/Haoua01/Africa-money-map/blob/main/codes/ORS/ors_isochrones.py)
    * Other operations are performed directly in QGIS
- Data: [data/Indicators/Fully_isochrone](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/Fully_isochrone)

---

### Section 4.3 Indicator 3: a hybrid index of bank branch access 
- Operations are performed in QGIS 
- Data: [data/Indicators/Hybrid](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/Hybrid)

---

### Section 5 Assessing the determinants of bank branch access
- Codes and results:
    * Quarto document: [codes/Regression/regression.qmd](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Regression/regression.qmd)



## 3. Visualization
* Results are displayed as interactive dashboards in the website: www.africamoneymap.fr 


## 4. Acknowledgments
* OpenRouteService / HeiGIT – Distance matrices and isochrone generation
* The World Bank Living Standards Measurement Study (LSMS) - Regression analysis 

---

***This master thesis is a part of the project Africa Money Map, aiming at mapping the locations of financial services in Subsaharan Africa. The project is conducted by Haoua Ben Ali Abbo, master student at Université Paris-Dauphine and David Bounie, professor of economics at Télécom Paris, Institut Polytechnique de Paris. The project is funded by Institut Louis Bachelier.*** 
