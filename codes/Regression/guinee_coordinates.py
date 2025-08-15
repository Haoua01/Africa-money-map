import time
from geopy.geocoders import Nominatim

# Creating a dictionary with regions as keys and sectors as list of values
city_to_region = {
    "TOMBALI": ["CATIÓ", "KOMO", "BEDANDA", "CACINE", "QUEBO"],
    "QUINARA": ["BUBA", "EMPADA", "FULACUNDA", "TITE"],
    "OIO": ["BISSORA", "FARIM", "MANSABA", "MANSOA", "NHACRA"],
    "BIOMBO": ["QUINHAMEL", "PRABIS", "SAFIM"],
    "BOLAMA / BIJAGÓS": ["BOLAMA", "BUBAQUE", "CARAVELA", "UNO"],
    "BAFATÁ": ["BAFATÁ", "COSSÉ", "BAMBADINCA", "XITOLE", "CONTUBOEL", "GÂMAMUDO"],
    "GABÚ": ["BOÉ", "PITCHE", "GABÚ", "PIRADA", "SONACO"],
    "CACHEU": ["BIGÉNE", "BULA", "CAIÓ", "CANCHUNGO", "CACHEU", "S. DOMINGOS"],
    "BISSAU": ["BISAU"],
}




def get_coordinates(department_mapping, country):
        # Initialize geolocator
        geolocator = Nominatim(user_agent="department_coordinates")

        # Dictionary to store the coordinates
        department_coordinates = {}

        # Loop through the departments in the mapping
        for region, departments in department_mapping.items():
            for department in departments:
                try:
                    # Get the coordinates of the department
                    location = geolocator.geocode(f'{department}, {region}, {country}')
                    if location:
                        department_coordinates[department] = (location.latitude, location.longitude)
                    else:
                        print(f"Warning: {department} not found.")
                except Exception as e:
                    print(f"Error geocoding {department}: {e}")
                # Pause for a few seconds to avoid overloading the server
                time.sleep(1)

        return department_coordinates
    
department_coordinates = get_coordinates(city_to_region, 'Guinea-Bissau')
print(department_coordinates)


coordinates = {'CATIÓ': (11.2835568, -15.2547152), 'KOMO': (11.1964101, -15.3335452), 'BEDANDA': (11.348427, -15.112394), 'CACINE': (11.12915, -15.02007), 'QUEBO': (11.5388759, -14.7678444), 'BUBA': (11.591979, -14.994788), 'EMPADA': (11.541162, -15.227461), 'FULACUNDA': (11.774895, -15.1720999), 'TITE': (11.780287, -15.399514), 'BISSORA': (12.2235221, -15.4507416), 'FARIM': (12.4823646, -15.2196439), 'MANSABA': (12.2950027, -15.1712726), 'MANSOA': (12.06661, -15.316344), 'NHACRA': (11.9589273, -15.5378614), 'QUINHAMEL': (11.894183, -15.851309), 'PRABIS': (11.8005341, -15.7401575), 'SAFIM': (11.931923, -15.615397), 'BOLAMA': (11.57763, -15.475261), 'BUBAQUE': (11.3000802, -15.8312425), 'CARAVELA': (11.53941045, -16.329990159596093), 'UNO': (11.2459664, -16.16341), 'BAFATÁ': (12.1723403, -14.6555027), 'COSSÉ': (12.2552096, -14.5408101), 'BAMBADINCA': (12.023539, -14.860555), 'XITOLE': (11.7349442, -14.8144697), 'CONTUBOEL': (12.3755089, -14.5603502), 'BOÉ': (11.747412, -14.210941), 'PITCHE': (12.326137, -13.954994), 'GABÚ': (12.2819517, -14.2260818), 'PIRADA': (12.663468, -14.15473), 'SONACO': (12.3951689, -14.4838361), 'BIGÉNE': (12.439277, -15.535395), 'BULA': (12.108565, -15.711007), 'CAIÓ': (11.930685, -16.20014), 'CANCHUNGO': (12.066422, -16.031912), 'CACHEU': (12.274246, -16.1648911), 'S. DOMINGOS': (12.402654, -16.196593), 'BISAU': (11.861324, -15.583055)}