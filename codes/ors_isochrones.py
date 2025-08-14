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
directory_elevation_cache = './openrouteservice/elevation_cache' #path to your ORS cloned repository
branches_path = '/workspaces/Africa-money-map/data/ORS/branches_combined.geojson'
url = "http://localhost:8080/ors/v2/isochrones/driving-car" # OpenRouteService API URL 

"""data"""
# Load the YAML file
with open(config_path1, 'r') as file:
    config1 = yaml.safe_load(file)

with open(config_path2, 'r') as file:
    config2 = yaml.safe_load(file)

with open(branches_path, 'r') as f:
    branches_combined = geojson.load(f)

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


# Function to get isochrone for a given coordinate and time ranges
def get_isochrone_via_requests(coord, ranges):
    # The ORS API expects a list of locations, so we pass the coordinate as part of the list
    payload = {
        "locations": [coord],  # List of coordinates
        "range": ranges,  # Time ranges in seconds
        "profile": "driving-car"
        #"intersections":True
    }
    
    headers = {'Content-Type': 'application/json'}
    
    # Send the POST request to your local OpenRouteService instance
    response = requests.post(url, json=payload, headers=headers)
    #print(response.json())
    
    if response.status_code == 200:
        isochrone_data = response.json()  # Return the GeoJSON response directly
        return isochrone_data
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

# Function to extract coordinates from GeoJSON features
def extract_coordinates_from_geojson(geojson_data):
    coordinates = []
    for feature in geojson_data['features']:
        geometry = feature['geometry']
        
        if geometry['type'] == 'Point':
            # For Point geometry, directly extract longitude, latitude
            coordinates.append(geometry['coordinates'])
        elif geometry['type'] == 'MultiPoint':
            # For MultiPoint geometry, extract coordinates of each point
            coordinates.extend(geometry['coordinates'])
    
    return coordinates

def create_isochrones_geojson(country):

    #create a directory for the country if it does not exist
    country_dir = f'/workspaces/Africa-money-map/data/ORS/{country}'
    if not os.path.exists(country_dir):
        os.makedirs(country_dir)

    code = country_codes(country)

    clear_directory(directory_graphs)
    clear_directory(directory_elevation_cache)

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

    #get the values of the geojson file such that "country"= country
    geojson_data = [feature for feature in branches_combined['features'] if feature['properties']['country'] == country][0]
    total_branches = len(geojson_data['features'])
    country_geojson = {
        "type": "FeatureCollection",
        "features": geojson_data
    }

    # Extract coordinates from the GeoJSON
    coordinates= extract_coordinates_from_geojson(country_geojson)
    unique_coords = list(dict.fromkeys(map(tuple, coordinates)))

    list_of_ranges = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]  # Define the time ranges in minutes
    #list_of_ranges = [60]  # Define the time ranges in minutes
    for k in list_of_ranges:
        # Dictionary to store isochrone data with BQEAQ inside the properties
        isochrones = {
            "type": "FeatureCollection"
        }

        features=[]

        # Iterate over the coordinates and get isochrones for each
        for i, coord in enumerate(unique_coords):
            print(f"{i+1}/{total_branches}")

            time_range = [k * 60]
            isochrone_data = get_isochrone_via_requests(coord, ranges=time_range)
            features.append(isochrone_data['features'][0])

        # Add the features to the isochrones dictionary
        isochrones['features'] = features

        # Save the isochrones to a file in the country directory
        with open(os.path.join(country_dir, f'isochrones_{k}min.geojson'), 'w') as f:
            json.dump(isochrones, f, indent=4)
        print(f"Finished processing isochrones for {k} minutes for {country}.")

    # Start the Docker Compose process in detached mode
    subprocess.Popen(
        ['docker', 'compose', 'down'],
        cwd= directory_ors_docker,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(10)  # Wait for a few seconds to ensure the process has stopped


for country in ["benin", "togo", "guinee", "niger", "civ", "mali", "senegal", "burkina"]:
    print(f"Processing country: {country}")
    create_isochrones_geojson(country)
    print(f"Finished processing country: {country}\n")
