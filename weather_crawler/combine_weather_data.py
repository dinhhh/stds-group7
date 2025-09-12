import csv
import os
from collections import defaultdict

def calculate_average_weather_data():
    """
    Read weather data and calculate average values for each station and date
    """
    input_file = "data/weather/all_stations_20180101_20250911.csv"
    output_file = "data/weather/avg_weather_20180101_20250911.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store data for averaging
    # Key: (station, date), Value: list of records for that station-date combination
    station_date_data = defaultdict(list)
    
    print("Reading weather data...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                station = row.get('station', '') or ''
                date = row.get('YYYY-MM-DD', '') or ''
                
                station = station.strip() if station else ''
                date = date.strip() if date else ''
                
                if not station or not date:
                    continue
                
                # Extract numeric values, handling empty or invalid data
                try:
                    daily_rain_str = row.get('daily_rain', '') or ''
                    max_temp_str = row.get('max_temp', '') or ''
                    min_temp_str = row.get('min_temp', '') or ''
                    radiation_str = row.get('radiation', '') or ''
                    rh_tmax_str = row.get('rh_tmax', '') or ''
                    rh_tmin_str = row.get('rh_tmin', '') or ''
                    
                    daily_rain = float(daily_rain_str.strip()) if daily_rain_str.strip() else None
                    max_temp = float(max_temp_str.strip()) if max_temp_str.strip() else None
                    min_temp = float(min_temp_str.strip()) if min_temp_str.strip() else None
                    radiation = float(radiation_str.strip()) if radiation_str.strip() else None
                    rh_tmax = float(rh_tmax_str.strip()) if rh_tmax_str.strip() else None
                    rh_tmin = float(rh_tmin_str.strip()) if rh_tmin_str.strip() else None
                    
                    record = {
                        'daily_rain': daily_rain,
                        'max_temp': max_temp,
                        'min_temp': min_temp,
                        'radiation': radiation,
                        'rh_tmax': rh_tmax,
                        'rh_tmin': rh_tmin
                    }
                    
                    station_date_data[(station, date)].append(record)
                    
                except (ValueError, AttributeError):
                    # Skip rows with invalid numeric data
                    continue
    
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    
    print(f"Processing {len(station_date_data)} unique station-date combinations...")
    
    # Calculate averages and write to output file
    try:
        # Load station metadata to get state information
        stations_metadata = {}
        stations_file = "data/weather/metadata/stations.csv"
        
        try:
            with open(stations_file, 'r', encoding='utf-8') as stations_csvfile:
                stations_reader = csv.DictReader(stations_csvfile)
                for station_row in stations_reader:
                    station_id = station_row.get('station_id', '').strip()
                    state = station_row.get('state', '').strip()
                    if station_id and state:
                        stations_metadata[station_id] = state
        except Exception as e:
            print(f"Error reading stations metadata file: {e}")
            return
        
        # Group data by state and date
        state_date_data = {}
        
        for (station, date), records in station_date_data.items():
            state = stations_metadata.get(station)
            if not state:
                continue  # Skip stations without state information
            
            if (state, date) not in state_date_data:
                state_date_data[(state, date)] = []
            
            # Add all records for this station-date to the state-date group
            state_date_data[(state, date)].extend(records)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['state', 'YYYY-MM-DD', 'daily_rain', 'max_temp', 'min_temp', 'radiation', 'rh_tmax', 'rh_tmin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for (state, date), records in state_date_data.items():
                # Calculate averages for each field across all stations in the state for this date
                avg_record = {'state': state, 'YYYY-MM-DD': date}
                
                for field in ['daily_rain', 'max_temp', 'min_temp', 'radiation', 'rh_tmax', 'rh_tmin']:
                    values = [record[field] for record in records if record[field] is not None]
                    if values:
                        avg_record[field] = round(sum(values) / len(values), 2)
                    else:
                        avg_record[field] = None
                
                writer.writerow(avg_record)
    
    except Exception as e:
        print(f"Error writing output file: {e}")
        return
    
    print(f"✓ Successfully calculated averages and saved to {output_file}")

if __name__ == "__main__":
    calculate_average_weather_data()
