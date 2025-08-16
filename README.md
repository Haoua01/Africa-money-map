# Africa-money-map

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
    * Measures % of municipal area covered by at least one branch.
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

### Section 3.2 Data on bank branches
- **Codes**:
  * [Bank scraping and geocoding](https://github.com/Haoua01/Africa-money-map/tree/main/codes/Scraping/scraper)
  * [Combine data](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Scraping/combine_json.py) and [Shapefile generator](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Scraping/shapefile_generator.py)
- **Data**:
  * [Scraping data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Scraping_data)

---

### Section 3.3 Socio‑economic data
- **Codes**:
  * Household data cleaning is performed in QGIS
  * [Citypopulation codes](https://github.com/Haoua01/Africa-money-map/tree/main/codes/Regression/citypopulation)
- **Data**:
  * [Citypopulation data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Regression/citypopulation)
  * [Regression data (CSV)](https://github.com/Haoua01/Africa-money-map/blob/main/data/Regression/data_regression.csv)

---

### Section 4.1 Indicator 1: Floating Catchment Area (FCA) model
- **Codes**:
  * [ORS distance matrix generation](https://github.com/Haoua01/Africa-money-map/blob/main/codes/ORS/ors_time_distance_matrix.py)
  * [Index of access code](https://github.com/Haoua01/Africa-money-map/tree/main/codes/FCA)
- **Data**:
  * [FCA data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/FCA)

---

### Section 4.2 Indicator 2: Fully isochrones approach
- **Codes**:
  * [Isochrone generation](https://github.com/Haoua01/Africa-money-map/blob/main/codes/ORS/ors_isochrones.py)
- **Operations**: Intermediate workflows are executed directly in QGIS  
- **Data**:
  * [Fully isochrone data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/Fully_isochrone)

---

### Section 4.3 Indicator 3: Hybrid index of bank branch access
- **Operations**: Conducted in QGIS  
- **Data**:
  * [Hybrid indicator data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Indicators/Hybrid)

---

### Section 5 Assessing the determinants of bank branch access
- **Codes and results**:
  * [Citypopulation codes](https://github.com/Haoua01/Africa-money-map/tree/main/codes/Regression/citypopulation)
  * [Regression analysis (Quarto `.qmd`)](https://github.com/Haoua01/Africa-money-map/blob/main/codes/Regression/regression.qmd)
- **Data**:
  * [Citypopulation data](https://github.com/Haoua01/Africa-money-map/tree/main/data/Regression/citypopulation)
  * [Regression dataset (CSV)](https://github.com/Haoua01/Africa-money-map/blob/main/data/Regression/data_regression.csv)




## 3. Visualization
* Results are displayed as interactive dashboards in the website: www.africamoneymap.fr 


## 4. Acknowledgments
* OpenRouteService / HeiGIT – Distance matrices and isochrone generation
* The World Bank Living Standards Measurement Study (LSMS) - Regression analysis 
* This master thesis is a part of the project Africa Money Map, aiming at mapping the locations of financial services, focusing on bank branches, mobile money outlets, and microfinance agencies. The project is conducted by David Bounie, professor of economics at Télécom Paris, Institut Polytechnique de Paris, and Haoua Ben Ali Abbo, master student at Université Paris-Dauphine. The project is funded by Institut Louis Bachelier. 
