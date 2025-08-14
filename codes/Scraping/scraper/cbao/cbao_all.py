
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

# Path of the current .py file
current_file = Path(__file__).resolve()
current_dir = current_file.parent

# Replace with the actual URL you want to scrape
url = 'https://cbaobank.com/fr/qui-sommes-nous#succursales-168'  # Example URL, replace it with the actual one

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to hold the extracted data
    branches_data = []

    # Find all the card sections (each containing a branch)
    cards = soup.find_all('div', class_='card')

    # Extract data for each branch
    for card in cards:
        if card.find('button') is None:
            continue
        country_name = card.find('button').get_text(strip=True)  # Get country name from the button text
        branch_details = card.find('div', class_='card-body')
        
        # Extracting branch name and contact details
        branch_name = country_name.strip()  # Here, the country name itself acts as the branch name in this example
        address = branch_details.find_all('p')[1].get_text(strip=True)  # Address is in the second <p> tag
        contact = branch_details.find_all('p')[-1].get_text(strip=True)  # Contact info is in the last <p> tag

        branches_data.append({
            "Country": country_name,
            "Branch": branch_name,
            "Address": address,
            "Contact": contact
        })

    # Print the extracted data
    for branch in branches_data:
        print(branch)

    # Save the data to a JSON file
    #with open('branches_data.json', 'w', encoding='utf-8') as json_file:
        #json.dump(branches_data, json_file, ensure_ascii=False, indent=4)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
