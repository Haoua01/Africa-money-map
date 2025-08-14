import openrouteservice
import geojson
import requests
import json
import time
import yaml
import subprocess
import os
import shutil



"""paths"""
config_path1 = './openrouteservice/ors-docker/config/ors-config.yml'  #path to your ORS cloned repository
config_path2 = './openrouteservice/ors-config.yml'  #path to your ORS cloned repository
directory_ors_docker = './openrouteservice/ors-docker'  #path to your ORS cloned repository
directory_graphs = './openrouteservice/graphs/driving-car' #path to your ORS cloned repository
coordinates_path = '/workspaces/Africa-money-map/data/ORS/centroids_filtered.geojson'
neighbors_path = '/workspaces/Africa-money-map/data/UEMOA/all_neighbors_equipped_clean.json'
url = "http://localhost:8080/ors/v2/matrix/driving-car"

"""data"""
# Example GeoJSON data (replace with your actual GeoJSON file path)
with open(coordinates_path, 'r') as f:
    geojson_data = geojson.load(f)

with open(neighbors_path, 'r') as f:
    all_neighbors_equipped = json.load(f)

# Load the YAML file
with open(config_path1, 'r') as file:
    config1 = yaml.safe_load(file)

with open(config_path2, 'r') as file:
    config2 = yaml.safe_load(file)



def wait_for_log_pattern(cwd, log_pattern, max_attempts=300, delay=30):
    attempts = 0

    # Start the Docker Compose process in detached mode
    subprocess.Popen(
        ['docker', 'compose', 'up', '-d'],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(30)  # Wait for a few seconds to ensure the process has started

    while attempts < max_attempts:
        # Fetch the logs using 'docker compose logs'
        log_process = subprocess.Popen(
            ['docker', 'compose', 'logs', '--tail=10'],  # Fetch the last 10 lines of logs
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read the logs line by line
        stdout, _ = log_process.communicate()
        for line in stdout.splitlines():
            print(line)  # Optionally print the log line
            if log_pattern in line:  # This checks if log_pattern is anywhere in the line
                return True

        attempts += 1
        time.sleep(delay)

    # If the loop exits without finding the log pattern
    return False


def clear_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate over the files in the directory and delete them
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # Check if it's a file or a directory and delete accordingly
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {directory} does not exist.")


# Function to get distance_matrix for a given coordinate and time ranges
def get_distance_matrix_via_requests(coord):
    # The ORS API expects a list of locations, so we pass the coordinate as part of the list
    payload = {
        "locations": coord
    }
    print(f"Payload: {payload}")
    
    headers = {'Content-Type': 'application/json'}
    
    # Send the POST request to your local OpenRouteService instance
    response = requests.post(url, json=payload, headers=headers)
    #print(response.json())
    
    if response.status_code == 200:
        distance_matrix_data = response.json()  # Return the GeoJSON response directly
        return distance_matrix_data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def country_codes(country):
    #create else if for country_codes
    if country == "guinee":
        country_code = "guinea-bissau"
    elif country == "togo":
        country_code = "togo"
    elif country == "benin":
        country_code = "benin"
    elif country == "niger":
        country_code = "niger"
    elif country == "civ":
        country_code = "ivory-coast"
    elif country == "mali":
        country_code = "mali"
    elif country == "senegal":
        country_code = "senegal-and-gambia"
    elif country == "burkina":
        country_code = "burkina-faso"
    else:
        country_code = None

    return country_code

def create_ors_json(country):

    code = country_codes(country)
    distance_country = {}

    clear_directory(directory_graphs)

    """ors_config"""

    # Update the ORS configuration file for the current country
    config1['ors']['engine']['profile_default']['build']['source_file'] = f'{code}-latest.osm.pbf' #need to download the .osm.pbf file of the country from geofabrik and paste to ors-docker folder
    config1['ors']['engine']['profiles']['driving-car']['enabled'] = True
    config2['ors']['engine']['profile_default']['build']['source_file'] = f'{code}-latest.osm.pbf' #need to download the .osm.pbf file of the country from geofabrik and paste to ors-docker folder
    config2['ors']['engine']['profiles']['driving-car']['enabled'] = True

    with open(config_path1, 'w') as file:
        yaml.dump(config1, file)

    with open(config_path2, 'w') as file:
        yaml.dump(config2, file)

    """docker compose up"""

    # Define a more general log pattern to wait for
    log_pattern = 'Memory usage by profiles:'

    # Wait for the specific log pattern
    if wait_for_log_pattern(directory_ors_docker, log_pattern):
        print("Desired log pattern found. Continuing with the script...")
    else:
        print("Desired log pattern not found. Exiting the script.")

    """processing"""
    country_neighbors_data = all_neighbors_equipped[country]


    for city, neighbors in country_neighbors_data.items():
        distance_country[city] = {}
        #print(f"Processing city: {city} with {len(neighbors)} neighbors")
        city_coordinates = [feature['geometry']['coordinates'] for feature in geojson_data['features'] if feature['properties']['ADM3_FR'] == city]
        for neighbor, distance in neighbors.items():
            neighbor_coordinates = [feature['geometry']['coordinates'] for feature in geojson_data['features'] if feature['properties']['ADM3_FR'] == neighbor and feature['properties']['Country'] == country]
            if city_coordinates and neighbor_coordinates:
                #print([city_coordinates[0], neighbor_coordinates[0]])
                #distance=get_distance_matrix_via_requests([city_coordinates[0], neighbor_coordinates[0]])
                #city_lat, city_lon = city_coordinates[0]
                #neighbor_lat, neighbor_lon = neighbor_coordinates[0]
                coord= [city_coordinates[0], neighbor_coordinates[0]]
                time_travel = get_distance_matrix_via_requests(coord)
                if time_travel is None:
                    print(f"Error retrieving distance for {city} to {neighbor}. Skipping this pair.")
                    continue
                print(f"Distance for {city} to {neighbor}: {time_travel['durations'][0][1]} seconds")
                distance_country[city][neighbor] =  time_travel['durations'][0][1]  # Update the distance in the dictionary
                print(f"Distance for {city} to {neighbor}: {distance_country[city][neighbor]}")

    with open(f'/workspaces/Africa-money-map/data/ORS/{country}_time_travels_in_seconds.json', 'w') as f:
        json.dump(distance_country, f, indent=4)
    print(f"Distance matrix for {country} saved successfully.")
    
    # Start the Docker Compose process in detached mode
    subprocess.Popen(
        ['docker', 'compose', 'down'],
        cwd= directory_ors_docker,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(10)  # Wait for a few seconds to ensure the process has stopped


for country in all_neighbors_equipped.keys():
    print(f"Processing country: {country}")
    create_ors_json(country)
    print(f"Finished processing country: {country}\n")
    
