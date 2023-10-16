# Path: latency.py
import csv
import time
import requests
import os

# Load the environment variables
URL = os.getenv('APP_URL', "http://localhost")
PORT_POKEAPI = os.getenv('POKEAPI_PORT', "8000")
PORT_POKESTATS = os.getenv('POKESTATS_PORT', "8001")

# Define the URL of the app to measure
url = URL

# Define the routes
routes = ["/pokeapi", "/pokestats", "/pokeImages"]

# Define the interval between measurements (in seconds)
interval = os.getenv('INTERVAL', 2)

# Define the path to the CSV file
csv_path = os.getenv('CSV_PATH', r"C:\Users\olapu\SoftwareII\labs\lab-final\part1\Monitoring-Security\latency.csv")

# Define the CSV headers
csv_headers = ['timestamp', 'module', 'latency', 'status']


# Loop indefinitely
while True:
    # Open the CSV file for writing
    with open(csv_path, 'a', newline='') as csv_file:

        # Create a CSV writer
        csv_writer = csv.writer(csv_file)
        
        # Get the current timestamp
        timestamp = int(time.time())

        for route in routes:
            # Send an HTTP GET request to the app
            try:
                response = requests.get(url + ':' + PORT_POKEAPI + route + '?pokemon=pikachu')
                status = response.status_code
                latency = int(response.elapsed.total_seconds() * 1000)
            except:
                status = -1
                latency = -1
            
            # Write the data to the CSV file
            csv_writer.writerow([timestamp, route, latency, status])

    # Close the file
    csv_file.close()
    
    # Wait for the specified interval
    time.sleep(interval)