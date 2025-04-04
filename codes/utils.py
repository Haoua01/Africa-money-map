import numpy as np

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