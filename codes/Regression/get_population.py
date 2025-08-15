import requests
from bs4 import BeautifulSoup
import pandas as pd

countries=['benin','burkinafaso','ivorycoast', 'guineabissau', 'mali','niger','senegal','togo']

df_all={}

for country in countries:
    if country=='togo' or country=='senegal':
        url = f"https://www.citypopulation.de/en/{country}/mun/admin/"
    elif country=='ivorycoast':
        url = f"https://www.citypopulation.de/en/{country}/sub/admin/"
    elif country=='guineabissau':
        url="https://www.citypopulation.de/en/guineabissau/"
    else:
        url = f"https://www.citypopulation.de/en/{country}/admin/"

    # Send an HTTP request to get the content of the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the population and area data
    table = soup.find('table', {'class': 'data'})

    # Initialize lists to store data
    regions = []
    populations = []
    areas = []
    types_all=[]

    # Loop through the table rows (skip header row)
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            region_name = cells[0].get_text(strip=True)
            country =  cells[0].get_text(strip=True).replace(',', '')
            area = cells[2].get_text(strip=True).replace(',', '')  # Remove commas for numerical values
            types=cells[1].get_text(strip=True)
            population = cells[-2].get_text(strip=True).replace(',', '')  # Remove commas for numerical values
            
            # Append data to respective lists
            regions.append(region_name)

            populations.append(population)
            types_all.append(types)
            areas.append(area)
        

    df = pd.DataFrame({'Country': country, 'Region': regions, 'Type': types_all, 'Population': populations, 'Area': areas})
    df_all[f'{country}']=df

    print(df.head())

df_all=pd.concat(df_all.values())
print(df_all.shape)

#print(df_all[df_all['Country']=='Burkina Faso'].head())

# Export the data to a CSV file
#df_all.to_csv('/workspaces/Africa-money-map/data/Regression/uemoa_population.csv', index=False)

# Assuming df_all is already a DataFrame
df_clean = []

for index, row in df_all.iterrows():
    if row['Country'] == 'Burkina Faso' and row['Type'] == "Province":
        df_clean.append(row)
    elif row['Country'] == 'Côte d\'Ivoire [Ivory Coast]' and row['Type'] == "Sub-Prefecture":
        df_clean.append(row)
    elif row['Country'] == 'Sénégal' and row['Type'] == "Commune":
        df_clean.append(row)
    elif row['Country'] == 'Mali' and (row['Type'] == "Urban Commune" or row['Type'] == "Commune"):
        df_clean.append(row)
    elif row['Country'] == 'Niger' and (row['Type'] == "Arrondissement" or row['Type'] == "Commune"):
        df_clean.append(row)
    elif row['Country'] == 'Togo' and row['Type'] == "Commune":
        df_clean.append(row)
    elif row['Type'] == "Commune":  # General condition for Commune
        df_clean.append(row)

# Convert the filtered list of rows into a DataFrame
df_clean = pd.DataFrame(df_clean)

# Rename Region to ADM3_FR
df_clean.rename(columns={'Region': 'ADM3_FR'}, inplace=True)
df_clean.drop(columns=['Type'], inplace=True)
print(df_clean.shape)

# Export the cleaned data to a CSV file
output_path = '/workspaces/Africa-money-map/data/Regression/uemoa_population_clean.csv'
df_clean.to_csv(output_path, index=False)


