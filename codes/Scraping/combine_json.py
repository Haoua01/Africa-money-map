import json
import os

# Path to your folder with JSON files
folder_path = "/workspaces/Africa-money-map/codes/Scraping/scraper/result/json_data_all"

combined_data = []

# Loop through all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                combined_data.extend(data)  # If each file contains a list
            else:
                combined_data.append(data)  # If each file contains a single dict

# Save to a single JSON
#output_path = os.path.join(folder_path, "combined.json")
with open("/workspaces/Africa-money-map/codes/Scraping/branches_combined.json", "w", encoding="utf-8") as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

#print(f"Combined JSON saved to {output_path}")
