import csv
import requests
import os
from datetime import datetime
import time

def crawl_weather_data():
    """
    Crawl weather data for each station from the CSV file
    """
    # Path to the stations CSV file
    stations_file = "data/weather/metadata/stations.csv"
    
    # Check if stations file exists
    if not os.path.exists(stations_file):
        print(f"Error: File {stations_file} not found")
        return
    
    # Create output directory if it doesn't exist
    output_dir = "data/weather/"
    os.makedirs(output_dir, exist_ok=True)
    
    
    # API parameters
    base_url = "https://longpaddock.qld.gov.au/cgi-bin/silo/PatchedPointDataset.php"
    username = "dinhhung.0115@gmail.com"
    dataset = "Official"
    comment = "rxnjhg"
    format_type = "csv"
    start_date = "20180101"
    finish_date = "20250911"
    
    # Saved file
    output_file = os.path.join(output_dir, f"all_stations_{start_date}_{finish_date}.csv")
    
    # Read stations from CSV
    try:
        with open(stations_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            stations = list(reader)
    except Exception as e:
        print(f"Error reading stations file: {e}")
        return
    
    print(f"Found {len(stations)} stations to process")
    
    # Process each station
    for i, station in enumerate(stations, 1):
        station_id = station.get('station_id', '').strip()
        station_name = station.get('station_name', '').strip()
        
        if not station_id:
            print(f"Skipping station {i}: No station_id found")
            continue
        
        print(f"Processing station {i}/{len(stations)}: {station_name} (ID: {station_id})")
        
        # Build API URL
        params = {
            'station': station_id,
            'format': format_type,
            'start': start_date,
            'finish': finish_date,
            'username': username,
            'dataset': dataset,
            'comment': comment
        }
        
        try:
            # Make API request
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Append response to file
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  ✓ Successfully saved data to {output_file}")
            
            # Add small delay to be respectful to the API
            time.sleep(1.5)
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error fetching data for station {station_id}: {e}")
            continue
        except Exception as e:
            print(f"  ✗ Error saving data for station {station_id}: {e}")
            continue
    
    print("Weather data crawling completed!")

if __name__ == "__main__":
    crawl_weather_data()
