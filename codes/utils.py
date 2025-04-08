import numpy as np
import json

def normalize_scores(scores):
    min_score = min(scores.values())
    max_score = max(scores.values())
    if min_score == max_score:
        return {city: 0 for city in scores.keys()}  # Avoid division by zero
    else:
        return {city: (score - min_score) / (max_score - min_score) for city, score in scores.items()}

def format_scores(scores):
    return {city: round(score, 3) for city, score in scores.items()}  

def round_scores(scores):
    return {city: round(score) for city, score in scores.items()}  

def mean_scores(scores, mapping):
    # Calculate the mean ISIBF for each district
    type_mean_scores = {}

    for type_name, communes in mapping.items():
        # Calculate the mean ISIBF for the district
        total_isibf = sum(scores.get(commune, 0) for commune in communes)  # Sum ISIBF values of the departments
        mean_isibf = total_isibf / len(communes) if communes else 0  # Compute mean (avoid division by zero)
        type_mean_scores[type_name] = mean_isibf

    # Return the mean ISIBF for each district
    return type_mean_scores

def create_distance_dict(data):
    """
    Creates a nested dictionary where the key is city1 (InputID) and the value is 
    another dictionary with city2 (TargetID) as the key and the distance as the value.
    
    :param data: List of features containing 'InputID', 'TargetID', and 'Distance'
    :return: Nested dictionary
    """
    distance_dict = {}

    # Loop through each feature in the dataset
    for feature in data:
        city1 = feature["properties"]["InputID"]  # City1 (key)
        city2 = feature["properties"]["TargetID"]  # City2
        distance = feature["properties"]["Distance"]  # Distance between city1 and city2

        if city1 not in distance_dict:
            distance_dict[city1] = {}
        distance_dict[city1][city2] = distance
    print(f"Distance dictionary created with {len(distance_dict)} entries.")

    return distance_dict
    
def distance_matrix(shp, area, country):
    with open(f'Africa-money-map/data/{area}/{country}_distance_matrix.json',  'r') as f:
        neighbors_raw = [json.loads(line) for line in f if line.strip()]

    neighbors = create_distance_dict(neighbors_raw)

    with open(f'Africa-money-map/data/{area}/{country}_distance_matrix_clean.json', 'w', encoding='utf-8') as f: 
        json.dump(neighbors, f, ensure_ascii=False, indent=4)